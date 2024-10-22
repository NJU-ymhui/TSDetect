from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import get_method_body


class EmptyMethodInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__skip_list = ['{', '}', 'line_comment']  # 事实上根据协议line_comment在visit时就会跳过

    def get_smell_type(self):
        return SmellType.EMPTY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_declaration':  # constructor_declaration不在考虑范围内，即它可以为空
            block = get_method_body(node)
            if block is None:
                return
            self.smell = self.__check_is_empty_block(block)
            return
        return

    def __check_is_empty_block(self, block_node):
        for child in block_node.children:
            if child.type in self.__skip_list:
                continue
            else:
                return False
        return True
