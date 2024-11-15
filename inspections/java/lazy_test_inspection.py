from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import is_test_func


class LazyTestInspection(Inspection):
    # 在同一个测试方法内，待测类的变量的某一方法的一个重载只能调用一次，即测试一次
    def __init__(self, src_root=None):
        super().__init__()
        self.__has_invoked = []
        self.__methods_tobe_tested = []  # 待测方法名
        self.__variables_of_tested_class = []  # 类型是待测对象的局部变量
        self.__global_variables = []  # 全局变量，类型同上
        self.__class_tobe_tested = b''  # 待测类名
        self.__decl_method_name = b''  # 当前所在测试方法的名字
        self.__lazy_candidates = []
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
        return SmellType.LAZY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_declaration':
            # 考虑Java overloading的情况
            self.__has_invoked = []
            self.__variables_of_tested_class = []
            self.__is_test = is_test_func(node)
            for child in node.children:
                if child.type == 'identifier':
                    self.__decl_method_name = child.text  # 更新当前所在的方法名
                    break

        elif node.type == 'method_invocation':
            var_name = node.children[0].text
            if var_name in self.__lazy_candidates:
                # 此时调用了一个会引入smell的候选方法
                if self.__is_test:
                    self.smell = True
                else:
                    self.__lazy_candidates.append(self.__decl_method_name)
                return
            method_name = ''
            for i in range(len(node.children)):
                if node.children[i].type == '.':
                    var_name = node.children[i - 1].text
                    method_name = node.children[i + 1].text
                    break
            if method_name in self.__methods_tobe_tested:
                if var_name in self.__variables_of_tested_class or var_name in self.__global_variables:
                    # 是待测类类型的变量
                    # 有'.', 则下标为3的节点是参数列表
                    args = node.children[3].text  # 这里将问题简化,只考虑参数列表的字面量, 因为并没有做数据流分析
                    mixed = var_name + method_name + args
                    if mixed in self.__has_invoked:
                        if self.__is_test:
                            self.smell = True
                        else:
                            self.__lazy_candidates.append(self.__decl_method_name)
                        return
                    else:
                        self.__has_invoked.append(mixed)

        elif node.type == 'local_variable_declaration':
            ty = node.children[0].text
            if ty == self.__class_tobe_tested:
                for child in node.children:
                    if child.type == 'variable_declarator':
                        # 下标0是变量名
                        var_name = child.children[0].text
                        self.__variables_of_tested_class.append(var_name)

        elif node.type == 'field_declaration':
            for child in node.children:
                if child.type == 'type_identifier' and child.text != self.__class_tobe_tested:
                    break
                if child.type == 'variable_declarator':
                    var_name = child.children[0].text
                    self.__global_variables.append(var_name)
        return
