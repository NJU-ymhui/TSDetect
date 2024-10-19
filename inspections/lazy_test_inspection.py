from inspections.inspection import Inspection
from util.smell_type import SmellType


class LazyTestInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.LAZY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        # TODO
        return
