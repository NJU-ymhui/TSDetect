from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import is_bool


class RedundantAssertionInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__assert_functions = [b'Error', b'Errorf', b'Fatal', b'Log']

    def get_smell_type(self):
        return SmellType.REDUNDANT_ASSERTION

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'call_expression':
            for child in node.children:
                if child.type == 'selector_expression':
                    name_node = node.children[2]  # 节点2是调用方法名
                    func_name = name_node.text
                    if func_name in self.__assert_functions:
                        # 检查参数有没有true false null
                        for ch in node.children:
                            if ch.type == 'argument_list':
                                for param in ch.children:
                                    if is_bool(param.text):
                                        self.smell = True
                                        return
        return
