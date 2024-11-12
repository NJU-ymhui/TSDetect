from inspections.inspection import Inspection
from util.smell_type import SmellType


class SleepyTestInspection(Inspection):
    # 检测是否使用了Thread.sleep，可能会导致测试不稳定或耗时过长
    def __init__(self):
        super().__init__()
        self.__time = False

    def get_smell_type(self):
        return SmellType.SLEEPY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'import_spec' and node.text == b'"time"':
            self.__time = True
        if self.__time and node.type == 'selector_expression':
            if node.text == b'time.Sleep':
                self.smell = True
                return
        return
