from inspections.inspection import Inspection
from util.smell_type import SmellType


class ResourceOptimismInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.files = []

    def get_smell_type(self):
        return SmellType.RESOURCE_OPTIMISM

    def has_smell(self):
        return self.smell

    def visit(self, node):
        # TODO
        return
