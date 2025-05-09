from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.python.util import is_test_func


class UnknownTestInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.assert_functions = [b'assertTrue', b'assertFalse', b'assertNotNull', b'assertNull', b'assertNone', b'assertNotNone',
                                 b'assertArrayEquals', b'assertEquals', b'assertNotSame', b'assertSame',
                                 b'assertThrows', b'assertNotEquals']
        
    def get_smell_type(self):
        return SmellType.UNKNOWN_TEST

    def has_smell(self):
        return self.smell

    # def __visit_children(self, test_func_node):
    #     res = False
    #     for child in test_func_node.children:
    #         if child.type == 'call':
    #             if child.children[0].text in self.assert_functions:
    #                 return True
    #         else:
    #             res = res or self.__visit_children(child)
    #     return res
    def __visit_children(self, node):
        res = False
        for child in node.children:
            if child.type == 'call':
                function_name = child.child_by_field_name('function')
                if function_name and function_name.type in ['identifier', 'attribute']:
                    if function_name.text in self.assert_functions:
                        return True
            else:
                res = res or self.__visit_children(child)
        return res

    def visit(self, node):
        if self.smell:
            return
        if is_test_func(node):
            self.smell = not self.__visit_children(node)
            return
        return
