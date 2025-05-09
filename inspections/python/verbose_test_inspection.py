from inspections.inspection import Inspection
from util.smell_type import SmellType
from tree_sitter import Node


class VerboseTestInspection(Inspection):
    # 判断是否为冗长测试，若是则触发该smell
    def __init__(self, max_statements=10):
        super().__init__()
        self.max_statements = max_statements
        self.smell = False

    def get_smell_type(self):
        return SmellType.VERBOSE_TEST

    def has_smell(self):
        return self.smell

    def count_statements(self, node: Node) -> int:
        """
        计算函数定义节点主体部分中的换行符数量。
        """
        if node.type != 'function_definition':
            return 0

        # 获取函数体节点
        body_node = node.child_by_field_name('body')
        if not body_node:
            return 0

        # 计算函数体中换行符的数量
        body_text = body_node.text.decode('utf-8')
        line_count = body_text.count('\n')

        return line_count

    def visit(self, node):
        if self.smell:
            return
        # print(":::", self.count_statements(node))
        self.smell = self.count_statements(node) > self.max_statements
        return
