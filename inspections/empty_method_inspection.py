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
        if self.smell:
            return
        if node.type == 'block':
            print(node.text)
            print("parent::")
            print(node.parent.text)
        if node.type == 'method_declaration':  # constructor_declaration不在考虑范围内，即它可以为空
            i = 0
            block = node.children[i]
            print(":")
            while block.type != 'block' and i < len(node.children):
                block = node.children[i]
                print(block.type)
                i += 1
            if block.type == ';':
                # 说明这是一个带异常声明的函数声明，想要找到它的block需要从父节点开始
                parent = node.parent
                for candidate in parent.children:
                    if candidate.type == 'block':
                        block = candidate
                        break
            elif block.type != 'block':
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
