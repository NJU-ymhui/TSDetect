from util.smell_type import SmellType
from inspections.inspection import Inspection


class TestRunWarInspection(Inspection):
    # TODO 检测是否存在同一个文件资源被多个测试使用
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.TEST_RUN_WAR

    def has_smell(self):
        return self.smell

    def visit(self, node):
        # TODO
        return
