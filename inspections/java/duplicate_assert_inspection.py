from inspections.inspection import Inspection
from util.smell_type import SmellType


class DuplicateAssertInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__asserts_args = {}
        self.__assert_functions = [b'Error', b'Errorf', b'Fatal', b'Log']

    def get_smell_type(self):
        return SmellType.DUPLICATE_ASSERT

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'call_expression':
            # 形如b.Error("msg")
            func_name = b''
            for child in node.children:
                if child.type == 'selector_expression':
                    for grand_child in child.children:
                        if grand_child.type == 'field_identifier' and grand_child.text in self.__assert_functions:
                            func_name = grand_child.text
            args = node.children[1].text  # call_expression一共俩节点，一个selector_expression，一个argument_list
            if func_name in self.__assert_functions:
                if func_name in self.__asserts_args.keys():
                    args_list = self.__asserts_args[func_name]
                    if args in args_list:
                        self.smell = True
                    else:
                        args_list.append(args)
                        self.__asserts_args[func_name] = args_list
                else:
                    args_list = [args]
                    self.__asserts_args[func_name] = args_list

