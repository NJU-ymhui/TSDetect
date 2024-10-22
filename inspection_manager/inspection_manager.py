class InspectionManager:
    def __init__(self):
        self.__inspections = []

    def register(self, inspection):
        self.__inspections.append(inspection)

    def visit(self, node):
        for inspection in self.__inspections:
            inspection.visit(node)

    def get_smells(self):
        return [str(inspection.get_smell_type()) for inspection in self.__inspections if inspection.has_smell()]
