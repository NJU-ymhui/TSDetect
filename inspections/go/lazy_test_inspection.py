from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.go.util import get_method_body, is_test_func


class LazyTestInspection(Inspection):
    def __init__(self, max_calls=4):
        super().__init__()
        self.__lazy_candidates = []
        self.__invocation_cnt = 0
        self.__method_decl_name = b''
        self.__max_calls = max_calls  # 最多调用的方法数，若超过则认为可能存在潜在的smell

    def get_smell_type(self):
        return SmellType.LAZY_TEST

    def has_smell(self):
        return self.smell

    def __visit_4_test(self, node):
        # 测试函数满足smell置true
        for child in node.children:
            if child is None:
                return
            if child.type == 'call_expression':
                if child.children[0].type == 'identifier':
                    # child.children[0].text为函数名
                    if child.children[0].text in self.__lazy_candidates:
                        self.smell = True
                        return
                    else:
                        self.__invocation_cnt += 1
                        if self.__invocation_cnt > self.__max_calls:
                            self.smell = True
                            return
                elif child.children[0].type == 'selector_expression':
                    # child.children[0].children[2]为field名即函数名
                    if child.children[0].children[2].text in self.__lazy_candidates:
                        self.smell = True
                        return
                    else:
                        self.__invocation_cnt += 1
                        if self.__invocation_cnt > self.__max_calls:
                            self.smell = True
                            return
            self.__visit_4_test(child)

    def __visit_4_non_test(self, node, func_name):
        # 非测试函数若满足条件加入候选
        for child in node.children:
            if child is None:
                return
            if child.type == 'call_expression':
                if child.children[0].type == 'identifier':
                    # child.children[0].text为函数名
                    if child.children[0].text in self.__lazy_candidates:
                        self.__lazy_candidates.append(func_name)
                        return
                    else:
                        self.__invocation_cnt += 1
                        if self.__invocation_cnt > self.__max_calls:
                            self.__lazy_candidates.append(func_name)
                            return
                elif child.children[0].type == 'selector_expression':
                    # child.children[0].children[2]为field名即函数名
                    if child.children[0].children[2].text in self.__lazy_candidates:
                        self.__lazy_candidates.append(func_name)
                        return
                    else:
                        self.__invocation_cnt += 1
                        if self.__invocation_cnt > self.__max_calls:
                            self.__lazy_candidates.append(func_name)
                            return
            self.__visit_4_non_test(child, func_name)

    def visit(self, node):
        if self.smell:
            return
        # go确保了函数使用前一定先声明
        if node.type == 'function_declaration':
            self.__invocation_cnt = 0
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

