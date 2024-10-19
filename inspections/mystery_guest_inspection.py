from inspections.inspection import Inspection
from util.smell_type import SmellType


class MysteryGuestInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.mystery_guests = [
            b"Context",
            b"Cursor",
            b"File",
            b"FileOutputStream",
            b"HttpClient",
            b"HttpResponse",
            b"HttpPost",
            b"HttpGet",
            b"SoapObject",
            b"SQLiteOpenHelper",
            b"SQLiteDatabase"
        ]

    def get_smell_type(self):
        return SmellType.MYSTERY_GUEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'type_identifier':
            self.smell = node.text in self.mystery_guests
            return
        return
