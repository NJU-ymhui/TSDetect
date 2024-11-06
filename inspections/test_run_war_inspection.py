from util.smell_type import SmellType
from inspections.inspection import Inspection


class TestRunWarInspection(Inspection):
    # 检测是否存在同一个文件资源被多个测试使用
    def __init__(self):
        super().__init__()
        self.__file_args = []  # 记录出现过的文件路径名，重复出现则说明对应文件被多次占用

    def get_smell_type(self):
        return SmellType.TEST_RUN_WAR

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'object_creation_expression':
            obj_name = node.children[1].text
            if obj_name == b'File':
                arg_list = node.children[2]
                # 参数列表下标为1的节点是第一个参数即文件路径名
                file_path = arg_list.children[1].text
                if file_path in self.__file_args:
                    self.smell = True
                    return
                else:
                    self.__file_args.append(file_path)
        return
