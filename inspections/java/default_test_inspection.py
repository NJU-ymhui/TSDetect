from inspections.inspection import Inspection
from util.smell_type import SmellType
import re


class DefaultTestInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__pattern = r'.*[Ee]xample.*[Tt]est'

    def get_smell_type(self):
        return SmellType.DEFAULT_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        text = str(node.text)
        match = re.search(self.__pattern, text)
        self.smell = match
        return

