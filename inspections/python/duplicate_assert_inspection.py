from inspections.inspection import Inspection
from util.smell_type import SmellType


class DuplicateAssertInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__asserts_args = {}
        self.__assert_functions = [b'assertEqual', b'assertNotEqual', b'assertIs', b'assertIsNot', b'assertArrayEqual',
                                   b'assertNotSame', b'assertSequenceEqual', b'fail',
                                   b'assertSame', b'assertThrows', b'assertIn', b'assertNotIn', b'assertIsInstance',
                                   b'assertNotIsInstance', b'assertAlmostEqual', b'assertNotAlmostEqual', b'assertTrue',
                                   b'assertFalse', b'assertIsNone', b'assertIsNotNone', b'assertThat', b'assertLogs',
                                   b'assertNoLogs', b'assertGreater', b'assertGreaterEqual', b'assertLess',
                                   b'assertLessEqual', b'assertRegex', b'assertNotRegex', b'assertCountEqual',
                                   b'assertMultiLineEqual', b'assertListEqual', b'assertTupleEqual', b'assertSetEqual',
                                   b'assertDictEqual']

    def get_smell_type(self):
        return SmellType.DUPLICATE_ASSERT

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'call':
            func_name_node = node.children[0]
            func_name = func_name_node.text
            args = node.children[1].text
            # if args != b'({})':
            #     print(args)
            if func_name in self.__assert_functions:
                if func_name in self.__asserts_args.keys():
                    args_list = self.__asserts_args[func_name]
                    if args in args_list:
                        self.smell = True
                    else:
                        args_list.append(args)
                else:
                    args_list = [args]
                    self.__asserts_args[func_name] = args_list
