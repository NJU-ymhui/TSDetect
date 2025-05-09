from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.python.util import get_method_body


class EmptyMethodInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.skip_list = ['comment', 'line_comment', 'whitespace']  # 扩展跳过列表
        self.smell = False  # 添加初始定义

    def get_smell_type(self):
        return SmellType.EMPTY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'function_definition':
            block = get_method_body(node)
            if block is None:
                return
            self.smell = self.__check_is_empty_block(block)
            return
        return

    def __check_is_empty_block(self, block_node):
        # 如果函数体内只包含一个节点，并且该节点是 'pass' 语句，则认为是空方法
        if len(block_node.children) == 1 and block_node.children[0].type == 'pass':
            return True
        # 否则，继续检查其他子节点是否都是无关紧要的
        for child in block_node.children:
            if child.type in self.skip_list:
                continue
            else:
                return False
        return True
