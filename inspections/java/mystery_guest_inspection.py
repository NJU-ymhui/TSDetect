from inspections.inspection import Inspection
from util.smell_type import SmellType


class MysteryGuestInspection(Inspection):
    def __init__(self):
        super().__init__()
        # go中类似java的神秘来客只有os.File, net/http包和一个GitHub的数据库项目github.com/mattn/go-sqlite3
        self.__mystery_guests = [b'"os"', b'"net/http"', b'"github.com/mattn/go-sqlite3"']

    def get_smell_type(self):
        return SmellType.MYSTERY_GUEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'import_spec':
            self.smell = node.text in self.__mystery_guests
            return
        return
