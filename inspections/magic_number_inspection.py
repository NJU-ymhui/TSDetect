from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import is_number


class MagicNumberInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.assert_functions = [b'assertTrue', b'assertFalse', b'assertNotNull', b'assertNull',
                                 b'assertArrayEquals', b'assertEquals', b'assertNotSame', b'assertSame',
                                 b'assertThrows', b'assertNotEquals', b'assertThat']

    def get_smell_type(self):
        return SmellType.MAGIC_NUMBER

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_invocation':
            name_node = node.children[0]  # 节点0是调用方法名
            func_name = name_node.text
            if func_name in self.assert_functions:
                # 检查参数有没有数字
                for child in node.children:
                    if child.type == 'argument_list':
                        for param in child.children:
                            if is_number(param.text):
                                # 数字参数
                                self.smell = True
                                return
        return
