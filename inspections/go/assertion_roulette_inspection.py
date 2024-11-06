from inspections.inspection import Inspection
from util.smell_type import SmellType


class AssertionRouletteInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__assert_list = [b'Errorf', b'Error', b'Fatal', b'Log']

    def get_smell_type(self):
        return SmellType.ASSERTION_ROULETTE

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'call_expression':
            assertion = False
            for child in node.children:
                # selector_expression为结构体访问节点，形如t.Error
                if child.type == 'selector_expression':
                    for grandchild in child.children:
                        if grandchild.type == 'field_identifier' and grandchild.text in self.__assert_list:
                            assertion = True
                            break
                if child.type == 'argument_list' and assertion:
                    # 上述那些类似断言的参数
                    # print(len(child.children))
                    self.smell = len(child.children) == 3  # 仅有一个参数，这3个children分别是(, arg1, )
                    return



