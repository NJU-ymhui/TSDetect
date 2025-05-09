from inspections.inspection import Inspection
from util.smell_type import SmellType


class MysteryGuestInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.mystery_guests = [b"os", b"io", b"pathlib", b"shutil", b"tempfile", b"requests", b"http.client", b"urllib",
                                 b"httpx", b"sqlite3", b"pymysql", b"psycopg2", b"sqlalchemy", b"pymongo"]

    def get_smell_type(self):
        return SmellType.MYSTERY_GUEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'type_identifier' or node.type == 'identifier':
            self.smell = node.text in self.mystery_guests
            return
        return
