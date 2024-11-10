from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import get_method_body, index_of, get_class_body, get_class_name, is_test_class, is_test_func, is_print


class EagerTestInspection(Inspection):
    # 一个测试函数应当只测试一个待测方法，可以多次调用这个待测方法，但只能有一种待测方法
    def __init__(self):
        super().__init__()
        self.__lazy_candidates = []
        self.__variables_type = {}  # 只考虑局部变量，不考虑全局变量
        self.__type_method = {}
        self.__method_decl_name = b''

    def get_smell_type(self):
        return SmellType.EAGER_TEST

    def has_smell(self):
        return self.smell

    def __visit_method_invocation_4_test(self, statement):
        if statement.type == 'variable_declarator':
            parent = statement.parent
            if parent.type == 'local_variable_declaration':
                self.__variables_type[statement.children[0].text] = parent.children[0].text
        if statement.type == 'method_invocation':
            if is_print(statement.text):
                return
            # print(statement.text)
            # 作为Java中的待测函数，被测试的时候一般通过'.'访问
            index = index_of(statement, b'.')
            if index > 0:
                # 存在'.'，查看前面的变量是否是声明的待测类的类型
                if statement.children[index - 1].text in self.__variables_type.keys():
                    typ = self.__variables_type[statement.children[index - 1].text]
                    if len(self.__type_method) == 0:
                        self.__type_method[typ] = statement.children[index + 1].text  # .后面是方法
                    else:
                        if typ in self.__type_method.keys():
                            past_method = self.__type_method[typ]
                            if past_method != statement.children[index + 1].text:
                                # 调用了一个之前出现过的类型，但是调用了不同的方法，触发
                                self.smell = True
                                return
                        else:
                            # 该类型不在之前出现过的类型里，但又调用了他的方法
                            # 调用了一个新类型的方法，触发
                            self.smell = True
                            return
            else:
                func_name = statement.children[0]
                if func_name in self.__lazy_candidates:  # 调用了一个候选lazy，引入smell
                    self.smell = True
                    return
                # else: 调用了一个不会引入lazy smell的普通函数，那么认为不会引起test smell
        for child in statement.children:
            if not self.smell:
                self.__visit_method_invocation_4_test(child)

    def __visit_method_invocation_4_non_test(self, statement):
        if statement.type == 'variable_declarator':
            parent = statement.parent
            if parent.type == 'local_variable_declaration':
                self.__variables_type[statement.children[0].text] = parent.children[0].text
        if statement.type == 'method_invocation':
            index = index_of(statement, b'.')
            if index > 0:
                # 可能引入smell
                if statement.children[index - 1].text in self.__variables_type.keys():
                    # 该变量对应类型之前出现过
                    typ = self.__variables_type[statement.children[index - 1].text]
                    if len(self.__type_method) == 0:
                        self.__type_method[typ] = statement.children[index + 1].text  # .后面是方法
                    else:
                        # 看一下调用的方法是不是之前类型出现时测试的方法
                        if typ in self.__type_method.keys():
                            past_method = self.__type_method[typ]
                            if past_method != statement.children[index + 1].text:  # 当前的方法和之前方法比较，一样则没问题
                                # 否则加入候选（因为不是测试方法）
                                self.__lazy_candidates.append(self.__method_decl_name)
                                return
                        else:
                            # 该类型之前没有出现，但之前出现了别的待测类型，那么对这个新待测类型的任何方法调用都会触发
                            self.__lazy_candidates.append(self.__method_decl_name)
                            return

            else:
                func_name = statement.children[0]
                if func_name in self.__lazy_candidates:  # 该方法调用了另一个候选lazy，那么自己也成为候选（迭代调用的call graph）
                    self.__lazy_candidates.append(self.__method_decl_name)
                    return
        for child in statement.children:
            if not self.smell:
                self.__visit_method_invocation_4_non_test(child)

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'class_declaration':
            class_name = get_class_name(node)
            if is_test_class(class_name):
                # 测试类
                body = get_class_body(node)
                for child in body.children:  # 遍历类主体的各个子节点
                    if child.type == 'method_declaration':
                        self.__variables_type = {}
                        self.__type_method = {}
                        if child.children[0].type == 'modifiers':
                            self.__method_decl_name = child.children[2].text
                        else:
                            self.__method_decl_name = child.children[1].text
                        block = get_method_body(child)  # 方法的主体
                        if block is None:
                            return
                        if is_test_func(child):
                            for statement in block.children:  # 遍历方法block的各个子节点
                                if self.smell:
                                    return
                                # print(statement.type, statement.text)
                                self.__visit_method_invocation_4_test(statement)
                        else:
                            # 普通的方法声明，我们看一下它会不会引入可能的smell，若可能，当他被调用，触发smell
                            for statement in block.children:
                                if self.smell:
                                    return
                                self.__visit_method_invocation_4_non_test(statement)
