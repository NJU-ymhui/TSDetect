from inspections.inspection import Inspection
from util.smell_type import SmellType
from tree_sitter import Node


class VerboseVariableInspection(Inspection):
    # 判断函数体中的变量个数是否超过限制，若超过则触发该smell
    def __init__(self, limits=20):
        super().__init__()
        self.cnt = 0
        self.limits = limits
        self.smell = False

    def get_smell_type(self):
        return SmellType.VERBOSE_VARIABLE

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return

        if node.type == 'function_definition':
            self.cnt = 0
            self.count_variables(node)

        if node.type == 'assignment':
            self.cnt += 1
            if self.cnt >= self.limits:
                self.smell = True
                return

        for child in node.children:
            self.visit(child)

    def count_variables(self, node):
        for child in node.children:
            if child.type == 'assignment' or child.type == 'variable_declarator':
                self.cnt += 1
                if self.cnt >= self.limits:
                    self.smell = True
                    return
            self.count_variables(child)

