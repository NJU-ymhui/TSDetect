from util.smell_type import SmellType
from inspections.inspection import Inspection


class NonDeterministicInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.NON_DETERMINISTIC_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        # TODO
        return
