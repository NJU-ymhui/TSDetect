from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import is_variable_decl, print_child


class ResourceOptimismInspection(Inspection):
    # TODO 暂时无法解决一个方法接受File参数，然后方法内部检验 /不检验file的存在，之后一个File变量通过该方法传进去，暂时判断不了
    def __init__(self):
        super().__init__()
        self.current_method = 0  # 0表示成员变量
        self.unchecked_files = {0: []}
        self.checked_files = {0: []}  # 事实上只有成员变量可能用到这个数据结构，因为只有成员变量可能先使用再声明，而局部变量不可能
        self.check_methods = [b'exists', b'notExists', b'isFile']

    def get_smell_type(self):
        return SmellType.RESOURCE_OPTIMISM

    def has_smell(self):
        for key in self.unchecked_files.keys():
            if len(self.unchecked_files[key]) > 0:
                return True
        return False

    def __is_file_decl(self, decl_node):
        b = False
        for child in decl_node.children:
            if child.type == 'type_identifier':
                return child.text == b'File'
            b = b or self.__is_file_decl(child)
            if b:
                return True
        return b

    def __get_params_name(self, node):
        res = []
        for child in node.children:
            if child.type == 'identifier':
                res.append(child.text)
                continue
            res.extend(self.__get_params_name(child))
        return res

    def visit(self, node):
        if node.type == 'method_declaration':
            self.current_method += 1
            self.unchecked_files[self.current_method] = []
            self.checked_files[self.current_method] = []
            return
        if is_variable_decl(node):
            if node.parent.type == 'field_declaration':
                area = 0
            else:
                area = self.current_method
            if self.__is_file_decl(node):
                file_names = self.__get_params_name(node)
                unchecked_list = self.unchecked_files[area]
                checked_list = self.checked_files[area]
                for file_name in file_names:
                    if file_name not in checked_list and file_names not in unchecked_list:
                        unchecked_list.append(file_name)
                        self.unchecked_files[area] = unchecked_list
            return
        if node.type == 'method_invocation':
            # print_child(node)
            # print()
            if node.children[1].text == b'.':
                callee = node.children[0].text
                method = node.children[2].text
                if method in self.check_methods:
                    # 这是一个资源检测的方法
                    unchecked_list = self.unchecked_files[self.current_method]
                    if callee in unchecked_list:
                        unchecked_list.remove(callee)
                        self.unchecked_files[self.current_method] = unchecked_list
                    else:
                        unchecked_list = self.unchecked_files[0]
                        if callee in unchecked_list:
                            unchecked_list.remove(callee)
                            self.unchecked_files[0] = unchecked_list
                        else:
                            # callee既不在当前函数的列表里，也不在当前类的成员变量里，说明声明在下面，在checked_files里存一下
                            checked_list = self.checked_files[0]
                            checked_list.append(callee)
                            self.checked_files[0] = checked_list
        return
