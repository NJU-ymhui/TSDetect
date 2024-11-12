from util.smell_type import SmellType
from inspections.inspection import Inspection


class LogsInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__logs_tot = 0  # 统计所有的log(其实是print)语句
        self.__logs = [b'System.out.println', b'System.out.print', b'System.err.println', b'System.err.print']

    def get_logs_num(self):
        return self.__logs_tot

    def logs_info(self):
        return True

    def get_smell_type(self):
        return SmellType.LOGS_EXISTS

    def has_smell(self):
        return self.__logs_tot > 0

    def visit(self, node):
        if node.type == 'method_invocation' and True in [node.text.startswith(call) for call in self.__logs]:
            self.__logs_tot += 1

