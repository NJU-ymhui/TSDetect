from util.smell_type import SmellType
from inspections.inspection import Inspection


class TestRunWarInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.TEST_RUN_WAR

    def has_smell(self):
        return self.smell

    def visit(self, node):
        # TODO
        return
