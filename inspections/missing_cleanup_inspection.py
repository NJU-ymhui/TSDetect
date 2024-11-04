from util.smell_type import SmellType
from inspections.inspection import Inspection


class MissingCleanupInspection(Inspection):
    # 缺少适当的清理操作导致副作用影响其他测试，判定依据为有@Before(一般对应setUp)但没有@After(一般对应tearDown)且有多于一个测试方法
    def __init__(self):
        super().__init__()
        self.__test_cnt = 0
        self.__before = False
        self.__after = False

    def get_smell_type(self):
        return SmellType.MISSING_CLEANUP

    def has_smell(self):
        return self.__test_cnt > 1 and self.__before and not self.__after

    def visit(self, node):
        if node.type == 'marker_annotation':
            if node.text == b'@Test' or node.text == b'@test':
                self.__test_cnt += 1
            elif node.text == b'@Before':
                self.__before = True
            elif node.text == b'@After':
                self.__after = True
