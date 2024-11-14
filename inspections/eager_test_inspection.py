from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import get_method_body, index_of, get_class_body, get_class_name, is_test_class, is_test_func, is_print


class EagerTestInspection(Inspection):
    # eager test指在同一个测试方法里测试了多个待测函数
    # 这个想要准确检验必须接受待测源代码文件，解析其中的待测函数
    def __init__(self, max_calls=4, src_file_root=None):
        super().__init__()
        self.__lazy_candidates = []
        self.__invocation_cnt = 0
        self.__method_decl_name = b''
        self.__max_calls = max_calls  # 最多调用的方法数，若超过则认为可能存在潜在的smell
        self.__func_tobe_test = []
        self.__cur_tested = b''
        if src_file_root is not None:
            # 这里初始化识别所有待测函数
            for child in src_file_root.children:
                if child.type == 'function_declaration':
                    name = child.children[1].text
                    self.__func_tobe_test.append(name)

    def get_smell_type(self):
        return SmellType.EAGER_TEST

    def has_smell(self):
        return self.smell

    def __visit_4_test(self, node):
        # 测试函数满足smell置true
        if self.smell:
            return
        for child in node.children:
            if self.smell:
                return
            if child is None:
                return
            if child.type == 'call_expression':
                if child.children[0].type == 'identifier':
                    # child.children[0].text为函数名
                    name = child.children[0].text
                    if name in self.__lazy_candidates:
                        self.smell = True
                        return
                    else:
                        if name in self.__func_tobe_test:
                            # 可能引入smell
                            if self.__cur_tested == b'':
                                self.__cur_tested = name
                            elif self.__cur_tested != name:
                                self.smell = True
                                return
            self.__visit_4_test(child)

    def __visit_4_non_test(self, node, func_name):
        # 非测试函数若满足条件加入候选
        if func_name in self.__lazy_candidates:
            return
        for child in node.children:
            if func_name in self.__lazy_candidates:
                return
            if child is None:
                return
            if child.type == 'call_expression':
                if child.children[0].type == 'identifier':
                    # child.children[0].text为函数名
                    name = child.children[0].text
                    if name in self.__lazy_candidates:
                        self.__lazy_candidates.append(func_name)
                        return
                    if name in self.__func_tobe_test:
                        if self.__cur_tested == b'':
                            self.__cur_tested = name
                        elif self.__cur_tested != name:
                            self.__lazy_candidates.append(func_name)
                            return
            self.__visit_4_non_test(child, func_name)

    def visit(self, node):
        if self.smell:
            return
        # go确保了函数使用前一定先声明
        if node.type == 'function_declaration':
            self.__cur_tested = b''
            if is_test_func(node):
                block = get_method_body(node, 'go')
                if block is None:
                    return
                self.__visit_4_test(block)
            else:
                # 不是测试方法但是引入过多的方法调用，当测试方法调用它时，引入smell
                block = get_method_body(node, 'go')
                if block is None:
                    return
                func_name = node.children[1].text
                self.__visit_4_non_test(block, func_name)

