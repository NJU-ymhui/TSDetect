from inspections.inspection import Inspection
from util.smell_type import SmellType
from tree_sitter import Node


class TestRunWarInspection(Inspection):
    # 检测是否存在同一个文件资源被多个测试使用
    def __init__(self):
        super().__init__()
        self.__file_args = []  # 记录出现过的文件路径名，重复出现则说明对应文件被多次占用
        self.smell = False

    def get_smell_type(self):
        return SmellType.TEST_RUN_WAR

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return

        if node.type == 'call':
            value = node.text.decode('utf-8')
            if value.startswith('open('):
                name = value.split(',', 1)[0]
                if name in self.__file_args:
                    self.smell = True
                    return
                else:
                    self.__file_args.append(name)

        for child in node.children:
            self.visit(child)
