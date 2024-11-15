from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.util import get_method_body, index_of, get_class_body, get_class_name, is_test_class, is_test_func, is_print


class EagerTestInspection(Inspection):
    # eager test指在同一个测试方法里测试了多个待测函数
    # 这个想要准确检验必须接受待测源代码文件，解析其中的待测函数
    def __init__(self, src_file_root=None):
        super().__init__()
        self.__eager_candidates = []  # 可能触发eager smell的候选函数, 因为它们不是测试方法
        self.__method_decl_name = b''  # 当前所在测试方法的名字
        self.__func_tobe_test = []  # 待测函数
        self.__cur_tested = b''  # 当前测试方法正在测试的函数
        self.__is_test = True
        if src_file_root is not None:
            # 这里初始化识别所有待测函数
            for child in src_file_root.children:
                if child.type == 'function_declaration':
                    name = child.children[1].text
                    self.__func_tobe_test.append(name)

    def get_smell_type(self):
        return SmellType.EAGER_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        # go确保了函数使用前一定先声明
        if node.type == 'function_declaration':
            self.__cur_tested = b''
            self.__is_test = is_test_func(node)
            self.__method_decl_name = node.children[1].text  # 节点1是声明的函数名

        elif node.type == 'call_expression':
            # 我们对于待测函数的调用一定是func()的形式, 若有a.func()我们依然选择节点0.这样一定不满足in的条件,与我们的排除目的吻合
            func_name = node.children[0].text
            if func_name in self.__func_tobe_test:
                if self.__cur_tested == b'':
                    self.__cur_tested = func_name
                elif self.__cur_tested != func_name:
                    if self.__is_test:
                        self.smell = True
                        return
                    else:
                        self.__eager_candidates.append(self.__method_decl_name)
            elif func_name in self.__eager_candidates:
                # 当前函数调用了一个触发过smell的非测试方法, 若当前函数是测试方法则触发
                if self.__is_test:
                    self.smell = True
                    return
                else:
                    self.__eager_candidates.append(self.__method_decl_name)
