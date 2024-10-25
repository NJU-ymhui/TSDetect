from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.java.util import is_method_decl, count_statements


class VerboseTestInspection(Inspection):
    # 判断是否为冗长测试，若是则触发该smell
    def __init__(self, max_statements=14):
        super().__init__()
        self.__max_statements = max_statements

    def get_smell_type(self):
        return SmellType.VERBOSE_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if is_method_decl(node):
            # print(":::", count_statements(node))
            self.smell = count_statements(node) > self.__max_statements
        return
