from inspections.inspection import Inspection
from util.smell_type import SmellType


class SleepyTestInspection(Inspection):
    # 检测是否使用了Thread.sleep，可能会导致测试不稳定或耗时过长
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.SLEEPY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_invocation':
            thread, sleep = False, False
            for child in node.children:
                if child.text == b'Thread':
                    thread = True
                if child.text == b'sleep':
                    sleep = True
                self.smell = thread and sleep
                if self.smell:
                    return
        return

