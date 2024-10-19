from inspections.inspection import Inspection
from util.smell_type import SmellType


class EmptyMethodInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.skip_list = ['{', '}', 'line_comment']  # 事实上根据协议line_comment在visit时就会跳过

    def get_smell_type(self):
        return SmellType.EMPTY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        # TODO: 有bug
        if self.smell:
            return
        if node.type == 'block':
            print(node.text)
            print("parent::")
            print(node.parent.text)
        if node.type == 'method_declaration':  # constructor_declaration不在考虑范围内，即它可以为空
            # i = 0
            # block = node.children[i]
            # print(":")
            # while block.type != 'block' and i < len(node.children):
            #     block = node.children[i]
            #     print(block.type)
            #     i += 1
            # if block.type != 'block':
            #     return
            block = node.child_by_field_name('body')
            if block:
                print(block.text)  # 打印方法主体的 S-expression
            else:
                print(block)
                return
            self.smell = self.__check_is_empty_block(block)
            return
        return

    def __check_is_empty_block(self, block_node):
        for child in block_node.children:
            if child.type in self.skip_list:
                continue
            else:
                return False
        return True
