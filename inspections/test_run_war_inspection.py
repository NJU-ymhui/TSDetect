from util.smell_type import SmellType
from inspections.inspection import Inspection


class TestRunWarInspection(Inspection):
    # 要是在全局作用域打开一个文件就没辙了
    def __init__(self):
        super().__init__()
        self.__file2func = {}
        self.__cur_func = ''

    def get_smell_type(self):
        return SmellType.TEST_RUN_WAR

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'func_declaration':
            self.__cur_func = node.text
        if node.type == 'call_expression' and node.children[0].type == b'selector_expression':
            call = node.children[0]
            # 检测是不是os.Open或os.OpenFile
            if call.text == b'os.Open' or call.text == b'os.OpenFile':
                # 获取参数之一文件路径
                arg_list = node.children[1]  # 获取参数列表子节点
                file_path = arg_list.children[1].text  # 下标1的子节点是路径
                if file_path in self.__file2func.keys():
                    if self.__cur_func != self.__file2func[file_path]:
                        self.smell = True
                        return
                else:
                    self.__file2func[file_path] = self.__cur_func
                    return
