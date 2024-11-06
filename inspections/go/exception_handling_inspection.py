from inspections.inspection import Inspection
from util.smell_type import SmellType


class ExceptionHandlingInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__exceptions = [b'panic', b'recover']
        self.__errors = b''

    def get_smell_type(self):
        return SmellType.EXCEPTION_HANDLING

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'import_spec' and node.text == b'"errors"':
            self.__errors = b'errors.New'
        if node.text in self.__exceptions or node.text == self.__errors:
            self.smell = True
            return
