from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import get_method_body, index_of, get_class_body, get_class_name, is_test_class, is_test_func, is_print


class EagerTestInspection(Inspection):
    # TODO 有一个问题:Java支持先使用后声明,这导致看你先调用一个candidate但是在这之后candidate才被声明,那么在调用的时候是不知道它可能引入smell
    # TODO 考虑用回调的方法或者回头看的方法解决
    # 一个测试函数应当只测试一个待测方法，可以多次调用这个待测方法，但只能有一种待测方法
    # 不必考虑java overloading, 认为是同一种方法, 因为没有数据流分析不好区分
    def __init__(self, src_root=None):
        super().__init__()
        self.__eager_candidates = []  # 可能引入smell的非测试方法
        self.__variables_of_tested_class = []  # 只考虑局部变量，不考虑全局变量
        self.__cur_tested = b''  # 当前测试方法测试的待测方法
        self.__method_decl_name = b''  # 测试类中声明的方法名
        self.__class_tobe_tested = b''  # 待测类名
        self.__methods_tobe_tested = []  # 待测类中的待测方法
        self.__is_test = True
        class_body = None
        if src_root is not None:
            for child in src_root.children:
                if child.type == 'class_declaration':
                    for child_child in child.children:
                        if child_child.type == 'identifier':
                            self.__class_tobe_tested = child_child.text
                        if child_child.type == 'class_body':
                            class_body = child_child
                            break
                    break
            if class_body is not None:
                for child in class_body.children:
                    if child.type == 'method_declaration':
                        for method in child.children:
                            if method.type == 'identifier':
                                name = method.text
                                self.__methods_tobe_tested.append(name)

    def get_smell_type(self):
        return SmellType.EAGER_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_declaration':
            self.__is_test = is_test_func(node)
            self.__variables_of_tested_class = []
            self.__cur_tested = b''
            for child in node.children:
                if child.type == 'identifier':
                    self.__method_decl_name = child.text
        elif node.type == 'local_variable_declaration':
            ty = node.children[0].text
            if ty == self.__class_tobe_tested:
                for child in node.children:
                    if child.type == 'variable_declarator':
                        # 下标0是变量名
                        var_name = child.children[0].text
                        self.__variables_of_tested_class.append(var_name)
        elif node.type == 'method_invocation':
            var_name = node.children[0].text  # 0号节点要么是func如果是func(), 要么是变量名var如果是var.method()
            method_name = ''  # 要么a.method(), 要么func()
            if var_name in self.__eager_candidates:  # 若是func()且匹配候选则触发smell(因为in candidates的一定是func())
                if self.__is_test:
                    self.smell = True
                    return
                self.__eager_candidates.append(self.__method_decl_name)
                return
            # 提取第一组变量名和方法名, 若v.a().b().c()..., 不管了
            for i in range(len(node.children)):
                if node.children[i].type == '.':
                    var_name = node.children[i - 1].text
                    method_name = node.children[i + 1].text
                    break
            if method_name in self.__methods_tobe_tested:
                if var_name in self.__variables_of_tested_class:
                    # 是待测类的一个变量, 下面检验该变量调用的方法是否和当前测试的方法一致
                    if self.__cur_tested == b'':
                        # 还没识别到待测方法
                        self.__cur_tested = method_name
                    elif self.__cur_tested != method_name:
                        # 调用的测试方法和之前测的不一致, 说明测试了多个待测方法, 需要触发smell
                        if self.__is_test:
                            self.smell = True
                            return
                        self.__eager_candidates.append(self.__method_decl_name)
                        return
