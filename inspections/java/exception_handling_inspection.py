from inspections.inspection import Inspection
from util.smell_type import SmellType


class ExceptionHandlingInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.EXCEPTION_HANDLING

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'throw_statement' or node.type == 'catch_clause':
            self.smell = True
            return
        return

