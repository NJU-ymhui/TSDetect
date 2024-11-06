from util.smell_type import SmellType
from inspections.inspection import Inspection


class NonDeterministicInspection(Inspection):
    # 在测试中使用了线程相关操作或随机数
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.NON_DETERMINISTIC_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'type_identifier':
            if node.text == b'Random' or node.text == b'Thread':
                self.smell = True
                return
        elif node.type == 'method_invocation':
            if b'.' in node.text and node.children[0].text == b'Thread':  # 第一个节点是类
                self.smell = True
                return
