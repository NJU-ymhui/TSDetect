from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import is_number


class MagicNumberInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__assert_functions = [b'Error', b'Errorf', b'Fatal', b'Log']

    def get_smell_type(self):
        return SmellType.MAGIC_NUMBER

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        # go中类似assert作用的调用形如x.Error, x.Errorf, x.Fatal, x.Log 012下标
        # 这些都是selector_expression节点
        if node.type == 'selector_expression':
            name_node = node.children[2]  # 节点2是调用方法名
            func_name = name_node.text
            if func_name in self.__assert_functions:
                # 检查参数有没有数字
                parent = node.parent  # call_expression
                for child in parent.children:
                    if child.type == 'argument_list':
                        for param in child.children:
                            if is_number(param.text):
                                # 数字参数
                                self.smell = True
                                return
        return
