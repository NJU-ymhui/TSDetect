from util.smell_type import SmellType
from inspections.inspection import Inspection


class VerboseVariableInspection(Inspection):
    def __init__(self, limits=20):
        super().__init__()
        self.__var_cnt = 0
        self.__limits = limits

    def get_smell_type(self):
        return SmellType.VERBOSE_VARIABLE

    def has_smell(self):
        return self.smell

    def __step_in_decl(self, decl):
        if decl.type == 'identifier':
            self.__var_cnt += 1
        for child in decl.children:
            self.__step_in_decl(child)

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'function_declaration':
            if self.__var_cnt > self.__limits:
                self.smell = True
                return
            self.__var_cnt = 0
        if 'var_declaration' in node.type:
            self.__step_in_decl(node)
