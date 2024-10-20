from inspections.inspection import Inspection
from util.smell_type import SmellType


class SensitiveEqualityInspection(Inspection):
    # 检测代码中是否存在toString调用，有则认为存在smell
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.SENSITIVE_EQUALITY

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'method_invocation':
            for child in node.children:
                if child.text == b'toString':
                    self.smell = True
                    return
        return
