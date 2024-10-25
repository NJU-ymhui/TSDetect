from inspections.inspection import Inspection
from util.smell_type import SmellType


class EagerTestInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__freq = {}  # 生产函数调用次数
        self.__decls = []  # 加入该列表前判断是否在calls中出现过，因为Java允许先使用后声明

    def get_smell_type(self):
        return SmellType.EAGER_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'function_declaration':
            self.__freq = {}
            # Go下标为1的子节点是函数名  形如 func x
            method_name = node.children[1].text
            for func in self.__decls:
                self.__freq[func] = 0
            self.__decls.append(method_name)
        elif node.type == 'call_expression':
            func_name = node.children[0].text  # 函数调用就两种x.x和x()，取下标为0的内容，若是x.x则肯定匹配不上，若是x()则可能匹配
            if func_name in self.__freq.keys():  # 不用decls防止递归
                self.__freq[func_name] += 1
                if self.__freq[func_name] > 1:
                    self.smell = True
                    return
        return
