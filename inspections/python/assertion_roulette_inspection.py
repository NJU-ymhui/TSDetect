from inspections.inspection import Inspection
from util.smell_type import SmellType


class AssertionRouletteInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__one_param_assert = [b'fail']
        self.__two_params_assert = [b'assertTrue', b'assertFalse', b'assertIsNone', b'assertIsNotNone', b'assertThat', b'assertLogs', b'assertNoLogs', b'assertGreater', b'assertGreaterEqual', b'assertLess', b'assertLessEqual', b'assertRegex', b'assertNotRegex', b'assertCountEqual', b'assertMultiLineEqual', b'assertListEqual', b'assertTupleEqual', b'assertSetEqual', b'assertDictEqual']
        self.__three_params_assert = [b'assertEqual', b'assertNotEqual', b'assertIs', b'assertIsNot', b'assertArrayEqual', b'assertNotSame', b'assertSequenceEqual',
                                      b'assertSame', b'assertThrows', b'assertIn', b'assertNotIn', b'assertIsInstance', b'assertNotIsInstance']
        self.__four_params_assert = [b'assertAlmostEqual', b'assertNotAlmostEqual']

    def get_smell_type(self):
        return SmellType.ASSERTION_ROULETTE

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'call':
            # print(node)
            name_node = node.children[0]
            func_name = name_node.text
            self_func_name = str(func_name)[7:-1]
            self_func_name = self_func_name.encode()
            # print(func_name)
            # print(self_func_name)
            i = 0
            # print((len(node.children[1].children) - 1) // 2)
            # print(self_func_name)
            while(i<len(node.children[1].children)):
                #  print(f"i:{i}    !!&!&!&!&!&!    ", node.children[1].children[i].text.decode())
                i += 1
            if func_name in self.__one_param_assert or self_func_name in self.__one_param_assert:  # fail(), 没有参数则无法提供上下文信息，认为存在smell
                params_list_node = node.children[1]
                if (len(params_list_node.children) - 1) // 2 != 1:
                    self.smell = True
                    return
            elif func_name in self.__two_params_assert or self_func_name in self.__two_params_assert:  # 同理若没有消息参数则无法传递上下文信息
                params_list_node = node.children[1]
                if (len(params_list_node.children) - 1) // 2 != 2:
                    self.smell = True
                    return
            elif func_name in self.__three_params_assert or self_func_name in self.__three_params_assert:
                params_list_node = node.children[1]
                # print(params_list_node)
                if (len(params_list_node.children) - 1) // 2 != 3:
                    self.smell = True
                    return
            elif func_name in self.__four_params_assert or self_func_name in self.__four_params_assert:
                params_list_node = node.children[1]
                if (len(params_list_node.children) - 1) // 2 != 4:
                    self.smell = True
                    return
