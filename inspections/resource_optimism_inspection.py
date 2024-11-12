from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import is_global_var


class ResourceOptimismInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__global_err = []
        self.__local_err = []
        self.__check_methods = [b'os.IsNotExist', b'os.IsExist']

    def get_smell_type(self):
        return SmellType.RESOURCE_OPTIMISM

    def has_smell(self):
        return self.smell or len(self.__local_err) > 0 or len(self.__global_err) > 0

    # def __is_file_decl(self, decl_node):
    #     b = False
    #     for child in decl_node.children:
    #         if child.type == 'type_identifier':
    #             return child.text == b'File'
    #         b = b or self.__is_file_decl(child)
    #         if b:
    #             return True
    #     return b
    #
    # def __get_params_name(self, node):
    #     res = []
    #     for child in node.children:
    #         if child.type == 'identifier':
    #             res.append(child.text)
    #             continue
    #         res.extend(self.__get_params_name(child))
    #     return res

    def visit(self, node):
        if self.smell:
            return
        if node.type in ['short_var_declaration', 'var_declaration']:
            if len(node.children) >= 3:
                # 形如_, err := os.Open(...)的一定满足上述条件
                left = node.children[0]  # expression_list
                right = node.children[2]  # expression_list
                if len(left.children) != 3 or not (right.text.startswith(b'os.Open') or right.text.startswith(b'os.Stat')):
                    return
                err = left.children[2].text
                if is_global_var(node):
                    self.__global_err.append(err)
                else:
                    self.__local_err.append(err)
        elif node.type == 'function_declaration':
            self.smell = len(self.__local_err) > 0
            if self.smell:
                return
            self.__local_err = []
        elif node.type == 'call_expression':
            # 第一个子节点若是check_methods中之一，则进行了资源检测
            if node.children[0].text in self.__check_methods:
                for args in node.children:
                    if args.type == 'argument_list':
                        for arg in args.children:
                            if arg.type == 'identifier':
                                # 一步步找到函数的参数
                                if arg.text in self.__local_err:
                                    self.__local_err.remove(arg.text)
                                elif arg.text in self.__global_err:
                                    self.__global_err.remove(arg.text)
        elif node.type == 'binary_expression':
            # 形如err != nil
            err_candidate = node.children[0].text
            op = node.children[1]
            nil_candidate = node.children[2]
            if nil_candidate.type == 'nil' and op.type in ['!=', '==']:
                # 最后一个是nil, 比较符是!= 或 ==
                if err_candidate in self.__local_err:
                    self.__local_err.remove(err_candidate)
                elif err_candidate in self.__global_err:
                    self.__global_err.remove(err_candidate)

