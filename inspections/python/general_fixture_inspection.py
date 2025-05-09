from inspections.inspection import Inspection
from util.smell_type import SmellType


class GeneralFixtureInspection(Inspection):
    # 简单的看，只出现一次的局部变量必定是冗余的
    def __init__(self):
        super().__init__()
        # self.__global_vars = {}
        self.__local_vars = {}

    def get_smell_type(self):
        return SmellType.GENERAL_FIXTURE

    def has_smell(self):
        if self.smell:
            return self.smell
        # for glob in self.__global_vars.keys():
        #     if self.__global_vars[glob] == 0:
        #         return True
        for loc in self.__local_vars.keys():
            if self.__local_vars[loc] == 1:
                return True

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
        if node.type == 'function_definition':
            for loc in self.__local_vars.keys():
                if self.__local_vars[loc] == 1:
                    self.smell = True
                    return
            self.__local_vars = {}
        elif node.type == 'assignment':
            name = node.children[0].text  # 赋值式的第一个子节点是变量名
            if name in self.__local_vars.keys():
                self.__local_vars[name] += 1
            else:
                self.__local_vars[name] = 1
