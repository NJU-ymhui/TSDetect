from inspections.inspection import Inspection
from util.smell_type import SmellType


class GeneralFixtureInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__var_decl = ['var_declaration', 'short_var_declaration', 'const_declaration', 'parameter_declaration']
        self.__global_vars = {}
        self.__local_vars = {}

    def get_smell_type(self):
        return SmellType.GENERAL_FIXTURE

    def has_smell(self):
        if self.smell:
            return True
        for glob in self.__global_vars:
            if self.__global_vars[glob] == 0:
                return True
        # 最后一个函数的局部变量也没有验证
        for loc in self.__local_vars:
            if self.__local_vars[loc] == 0:
                return True
        return False

    def __visit_children(self, unused_dict, node):
        for child in node.children:
            if child.type == 'comment':
                continue
            if child.type == 'identifier' and child.text.decode('utf-8') in unused_dict:
                del unused_dict[child.text.decode('utf-8')]
                return unused_dict
            else:
                unused_dict = self.__visit_children(unused_dict, child)
        return unused_dict

    def __check_is_redundant(self):
        for local in self.__local_vars:
            if self.__local_vars[local] == 0:
                return True
        return False

    def __check_parent(self, node, parent_types):
        parent = node.parent
        if parent is None:
            return False
        if parent.type in parent_types:
            return True
        return self.__check_parent(parent, parent_types)

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'function_declaration':
            self.smell = self.__check_is_redundant()
            if self.smell:
                return
            self.__local_vars = {}
        elif node.type in self.__var_decl:
            if node.parent.type == 'source_file':
                # 全局变量
                for child in node.children:
                    if child.type == 'identifier':
                        self.__global_vars[child.text] = 0
            else:
                # 局部变量
                for child in node.children:
                    if child.type == 'identifier':
                        self.__local_vars[child.text] = 0
        else:
            if node.type == 'identifier' and not self.__check_parent(node, self.__var_decl):
                if node.text in self.__global_vars:
                    self.__global_vars[node.text] += 1
                elif node.text in self.__local_vars:
                    self.__local_vars[node.text] += 1
