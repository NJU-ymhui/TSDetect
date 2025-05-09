from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.python.util import is_number


class MagicNumberInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.assert_functions = [b'assertEqual', b'assertNotEqual', b'assertIs', b'assertIsNot', b'assertArrayEqual',
                                   b'assertNotSame', b'assertSequenceEqual', b'fail',
                                   b'assertSame', b'assertThrows', b'assertIn', b'assertNotIn', b'assertIsInstance',
                                   b'assertNotIsInstance', b'assertAlmostEqual', b'assertNotAlmostEqual', b'assertTrue',
                                   b'assertFalse', b'assertIsNone', b'assertIsNotNone', b'assertThat', b'assertLogs',
                                   b'assertNoLogs', b'assertGreater', b'assertGreaterEqual', b'assertLess',
                                   b'assertLessEqual', b'assertRegex', b'assertNotRegex', b'assertCountEqual',
                                   b'assertMultiLineEqual', b'assertListEqual', b'assertTupleEqual', b'assertSetEqual',
                                   b'assertDictEqual']

    def get_smell_type(self):
        return SmellType.MAGIC_NUMBER

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'call':
            name_node = node.children[0]  # 节点0是调用方法名
            func_name = name_node.text
            self_func_name = str(func_name)[7:-1]
            self_func_name = self_func_name.encode()
            if func_name in self.assert_functions or self_func_name in self.assert_functions:
                # 检查参数有没有数字
                for child in node.children:
                    if child.type == 'argument_list':
                        for param in child.children:
                            if is_number(param.text):
                                # 数字参数
                                self.smell = True
                                return
        return
