from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.go.util import is_test_func


class UnknownTestInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__assert_functions = [b'Error', b'Errorf', b'Log', b'Fatal']
        
    def get_smell_type(self):
        return SmellType.UNKNOWN_TEST

    def has_smell(self):
        return self.smell

    def __visit_children(self, test_func_node):
        res = False
        for child in test_func_node.children:
            if child.type == 'field_identifier':
                if child.text in self.__assert_functions:
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
