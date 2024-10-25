from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.go.util import is_print


class RedundantPrintInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.REDUNDANT_PRINT

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'selector_expression':
            self.smell = is_print(node.text, 'go')
            return
        return

