from util.smell_type import SmellType
from inspections.inspection import Inspection


class LogsInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__logs = [b'fmt.Println', b'fmt.Print', b'fmt.Printf', b'fmt.Fprintln', b'log.Println', b'log.Printf']
        self.__logs_cnt = 0

    def get_smell_type(self):
        return SmellType.LOGS_EXISTS

    def has_smell(self):
        return self.smell

    def logs_info(self):
        return True

    def visit(self, node):
        if node.type == 'call_expression':
            call_name = node.children[0].text
            if call_name in self.__logs:
                self.smell = True
                self.__logs_cnt += 1

    def get_logs_num(self):
        return self.__logs_cnt
