from util.smell_type import SmellType
from inspections.inspection import Inspection


class VerboseVariableInspection(Inspection):
    def __init__(self, limits=20):
        super().__init__()
        self.cnt = 0
        self.limits = limits

    def get_smell_type(self):
        return SmellType.VERBOSE_VARIABLE

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_declaration':
            self.cnt = 0
        if node.type == 'variable_declarator':
            self.cnt += 1
            if self.cnt >= self.limits:
                self.smell = True
                return
