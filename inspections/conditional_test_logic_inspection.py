from inspections.inspection import Inspection
from util.smell_type import SmellType


class ConditionalTestLogicInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.match_stmts = ["if_statement", "for_statement", "while_statement", "switch_expression",
                            "enhanced_for_statement"]

    def get_smell_type(self):
        return SmellType.CONDITIONAL_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type in self.match_stmts:
            self.smell = True
            return
