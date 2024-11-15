from inspections.inspection import Inspection
from util.smell_type import SmellType


class LazyTestInspection(Inspection):
    # lazy test测同一个方法多次
    def __init__(self, src_file_root=None):
        super().__init__()
        self.__freq = []  # 测试函数及其对应参数
        self.__is_test = True  # 先初始化为True防止进不去
        self.__cur_tested = b''
        self.__src_tobe_test = []
        if src_file_root is not None:
            for child in src_file_root.children:
                if child.type == 'function_declaration':
                    name = child.children[1].text
                    self.__src_tobe_test.append(name)

    def get_smell_type(self):
        return SmellType.LAZY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'function_declaration':
            self.__freq = []  # 每次遇到函数声明说明步入新的测试方法，清空
            # Go下标为1的子节点是函数名  形如 func x
            method_name = node.children[1].text
            if method_name.startswith(b'Test'):
                self.__is_test = True
            else:
                self.__is_test = False
        elif node.type == 'call_expression' and self.__is_test:
            func_name = node.children[0].text  # 函数调用就两种x.x和x()，取下标为0的内容，若是x.x则肯定匹配不上，若是x()则可能匹配
            if func_name in self.__src_tobe_test:
                # 这是一个待测函数
                # node的子节点0是函数名，1是参数列表
                arg_list = node.children[1].text
                mixed = func_name + arg_list
                if mixed in self.__freq:
                    self.smell = True
                    return
                self.__freq.append(mixed)
        return
