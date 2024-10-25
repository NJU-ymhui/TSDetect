from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.java.util import get_method_body, index_of, get_class_body, get_class_name, is_test_class, is_test_func, is_print


class LazyTestInspection(Inspection):
    def __init__(self, max_calls=3):
        super().__init__()
        self.__lazy_candidates = []
        self.__invocation_cnt = 0
        self.__method_decl_name = b''
        self.__max_calls = max_calls  # 最多调用的方法数，若超过则认为可能存在潜在的smell

    def get_smell_type(self):
        return SmellType.LAZY_TEST

    def has_smell(self):
        return self.smell

    def __visit_method_invocation_4_test(self, statement):
        if statement.type == 'method_invocation':
            if is_print(statement.text):
                return
            # print(statement.text)
            # 作为Java中的待测函数，被测试的时候一般通过'.'访问
            index = index_of(statement, b'.')
            if index > 0:
                if self.__invocation_cnt > self.__max_calls:
                    self.smell = True
                    return
                else:
                    self.__invocation_cnt += 1
            else:
                func_name = statement.children[0]
                if func_name in self.__lazy_candidates:
                    self.smell = True
                    return
                # else: 调用了一个不会引入lazy smell的普通函数，那么认为不会引起test smell
        for child in statement.children:
            if not self.smell:
                self.__visit_method_invocation_4_test(child)

    def __visit_method_invocation_4_non_test(self, statement):
        if statement.type == 'method_invocation':
            index = index_of(statement, b'.')
            if index > 0:
                if self.__invocation_cnt > self.__max_calls:
                    # 这个方法可能引入smell
                    # method_decl的下标为2节点是名字
                    self.__lazy_candidates.append(self.__method_decl_name)
                    return
                else:
                    self.__invocation_cnt += 1
            else:
                func_name = statement.children[0]
                if func_name in self.__lazy_candidates:
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
                        if child.children[0].type == 'modifiers':
                            self.__method_decl_name = child.children[2].text
                        else:
                            self.__method_decl_name = child.children[1].text
                        self.__invocation_cnt = 0
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

