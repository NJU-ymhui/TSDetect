from inspections.inspection import Inspection
from util.smell_type import SmellType


class ConstructorInitializationInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.CONSTRUCTOR_INITIALIZATION

    def has_smell(self):
        return self.smell

    # def visit(self, node):
    #     if self.smell:
    #         return
    #     if node.type == "constructor_declaration":
    #         self.smell = True
    #         return
    def visit(self, node):
        if self.smell:
            return
        if (node.type == "function_definition" and node.child_by_field_name('name').text == b'__init__') or node.type == "constructor_declaration":  # 转换后的节点类型和构造函数名称
            self.smell = True
            return
