class InspectionManager:
    def __init__(self):
        self.inspections = []

    def register(self, inspection):
        self.inspections.append(inspection)

    def visit(self, node):
        for inspection in self.inspections:
            inspection.visit(node)

    def get_smells(self):
        return [str(inspection.get_smell_type()) for inspection in self.inspections if inspection.has_smell()]
