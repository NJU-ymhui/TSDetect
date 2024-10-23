from inspections.inspection import Inspection
from util.smell_type import SmellType


class GeneralFixtureInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__global_vars = {}
        self.__local_vars = {}

    def get_smell_type(self):
        return SmellType.GENERAL_FIXTURE

    def has_smell(self):
        if self.smell:
            return self.smell
        for glob in self.__global_vars.keys():
            if self.__global_vars[glob] == 0:
                return True
        for loc in self.__local_vars.keys():
            if self.__local_vars[loc] == 0:
                return True

    def __visit_children(self, unused_dict, node):
        for child in node.children:
            if child.type == 'line_comment':
                continue
            if child.type == 'identifier' and child.text.decode('utf-8') in unused_dict:
                del unused_dict[child.text.decode('utf-8')]
                return unused_dict
            else:
                unused_dict = self.__visit_children(unused_dict, child)
        return unused_dict

    def __check_parent_type(self, node, parent_types):
        parent = node.parent
        if parent is None:
            return False
        if parent.type in parent_types:
            return True
        return self.__check_parent_type(parent, parent_types)

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'class_body':
            # 获取类中的所有字段
            for child in node.children:
                if child.type == 'field_declaration':
                    for field in child.children:
                        if field.type == 'variable_declarator':
                            self.__global_vars[field.text] = 0
        elif node.type == 'method_declaration':
            for loc in self.__local_vars.keys():
                if self.__local_vars[loc] == 0:
                    self.smell = True
                    return
            self.__local_vars = {}
        elif node.type == 'local_variable_declaration':
            for child in node.children:
                if child.type == 'variable_declarator':
                    for var in child.children:
                        if var.type == 'identifier':
                            self.__local_vars[var.text] = 0
        else:
            if node.type == 'identifier' and not self.__check_parent_type(node, ['field_declaration',
                                                                                 'local_variable_declaration']):
                if node.text in self.__local_vars.keys():
                    self.__local_vars[node.text] += 1
                elif node.text in self.__global_vars.keys():
                    self.__global_vars[node.text] += 1
