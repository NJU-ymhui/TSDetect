from util.smell_type import SmellType
from inspections.inspection import Inspection


class NonDeterministicInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.NON_DETERMINISTIC_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'call_expression' and node.children[0].type == 'selector_expression':
            call = node.children[0]  # selector_expression对应的节点 比如fmt.Println
            if call.children[0].text == b'rand':
                self.smell = True
                return
            if call.text == b'time.Sleep':
                self.smell = True
                return
