from inspections.inspection import Inspection
from util.smell_type import SmellType


class ConditionalTestLogicInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__match_stmts = ["if_statement", "switch_expression"]

    def get_smell_type(self):
        return SmellType.CONDITIONAL_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type in self.__match_stmts:
            self.smell = True
            return

