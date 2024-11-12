from util.smell_type import SmellType
from inspections.inspection import Inspection


class TATELeakageInspection(Inspection):
    # 涉及可能的状态共享，即有危险的全局变量
    def __init__(self):
        super().__init__()
        self.__global_vars = []
        self.__used_global_vars = {}
        self.__local_vars = []
        self.__tests_cnt = 0  # 测试方法的数量
        self.__decl_identifier_node = []
        self.__cur_func = ''

    def get_smell_type(self):
        return SmellType.TATE_LEAKAGE

    def has_smell(self):
        return self.smell and self.__tests_cnt > 1

    def __add_to_glob(self, node):
        if node.type == 'identifier':
            self.__decl_identifier_node.append(node)
            self.__global_vars.append(node.text)
            return
        for child in node.children:
            self.__add_to_glob(child)

    def __add_to_local(self, node):
        if node.type == 'identifier':
            self.__decl_identifier_node.append(node)
            self.__local_vars.append(node.text)
            return
        for child in node.children:
            self.__add_to_local(child)

    def visit(self, node):
        if self.smell:
            return
        if "var_declaration" in node.type:
            parent = node.parent
            if parent.type == 'source_file':
                # 全局变量
                self.__add_to_glob(node)
            else:
                # 局部变量
                self.__add_to_local(node)
        if node.type == 'function_declaration':
            self.__cur_func = node.children[1].text
            self.__tests_cnt += 1
            self.__local_vars = []
        if node.type == 'identifier' and node not in self.__decl_identifier_node:
            # 变量访问节点
            var_name = node.text
            if var_name in self.__local_vars:
                return
            elif var_name in self.__global_vars:
                if var_name not in self.__used_global_vars:
                    self.__used_global_vars[var_name] = self.__cur_func
                else:
                    # 全局变量曾被使用过，看看使用过的函数是不是当前函数，如果是则无妨，反之触发smell
                    if self.__used_global_vars[var_name] != self.__cur_func:
                        self.smell = True
                        return
