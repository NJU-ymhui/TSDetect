from inspections.inspection import Inspection
from util.smell_type import SmellType


class LazyTestInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__freq = 0  # 生产函数调用次数
        self.__decls = []  # 加入该列表前判断是否在calls中出现过，因为Java允许先使用后声明
        self.__calls = []  # 加入前判断是否在decls里，确定是否为生产方法调用

    def get_smell_type(self):
        return SmellType.LAZY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_declaration':
            # 下标为2的子节点是函数名
            method_name = node.children[2].text
            # TODO 需要考虑Java overloading的情况
            if method_name in self.__calls:
                self.__freq += 1
                if self.__freq > 1:
                    self.smell = True
                    return
            self.__decls.append(method_name)
        elif node.type == 'method_invocation':
            func_name = node.children[0].text
            if func_name in self.__decls:
                self.__freq += 1
                if self.__freq > 1:
                    self.smell = True
                    return
            self.__calls.append(func_name)
        return

