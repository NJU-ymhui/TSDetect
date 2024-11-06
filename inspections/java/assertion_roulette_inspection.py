from inspections.inspection import Inspection
from util.smell_type import SmellType


class AssertionRouletteInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__one_param_assert = [b'fail']
        self.__two_params_assert = [b'assertTrue', b'assertFalse', b'assertNull', b'assertNotNull', b'assertThat']
        self.__three_params_assert = [b'assertEquals', b'assertNotEquals', b'assertArrayEquals', b'assertNotSame',
                                    b'assertSame', b'assertThrows']

    def get_smell_type(self):
        return SmellType.ASSERTION_ROULETTE

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_invocation':
            name_node = node.children[0]
            func_name = name_node.text
            if func_name in self.__one_param_assert:  # fail(), 没有参数则无法提供上下文信息，认为存在smell
                params_list_node = node.children[1]
                if (len(params_list_node.children) - 1) // 2 < 1:
                    self.smell = True
                    return
            elif func_name in self.__two_params_assert:  # 同理若没有消息参数则无法传递上下文信息
                params_list_node = node.children[1]
                if (len(params_list_node.children) - 1) // 2 < 2:
                    self.smell = True
                    return
            elif func_name in self.__three_params_assert:
                params_list_node = node.children[1]
                if (len(params_list_node.children) - 1) // 2 < 3:
                    self.smell = True
                    return

