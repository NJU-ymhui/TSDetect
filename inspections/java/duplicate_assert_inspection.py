from inspections.inspection import Inspection
from util.smell_type import SmellType


class DuplicateAssertInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__asserts_args = {}
        self.__assert_functions = [b'assertTrue', b'assertFalse', b'assertNotNull', b'assertNull', b'assertArrayEquals',
                                   b'assertEquals', b'assertNotSame', b'assertSame', b'assertThrows', b'assertNotEquals']

    def get_smell_type(self):
        return SmellType.DUPLICATE_ASSERT

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_invocation':
            name_node = node.children[0]  # 节点0是调用方法名
            func_name = name_node.text
            args = node.children[1].text
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

