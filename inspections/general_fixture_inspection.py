from inspections.inspection import Inspection
from util.smell_type import SmellType


class GeneralFixtureInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.GENERAL_FIXTURE

    def has_smell(self):
        return self.smell

    def __visit_children(self, unused_dict, node):
        for child in node.children:
            if child.type == 'line_comment':
                continue
            if child.type == 'identifier' and child.text.decode('utf-8') in unused_dict:
                del unused_dict[child.text.decode('utf-8')]
                return unused_dict
            else:
                unused_dict = self.__visit_children(unused_dict, child)
        return unused_dict

    def visit(self, node):
        # TODO 目前只能识别类中的冗余字段，扩展到函数？
        if self.smell:
            return
        unused_fields = {}
        if node.type == 'class_body':
            # 获取类中的所有字段
            for child in node.children:
                if child.type == 'field_declaration':
                    for field in child.children:
                        if field.type == 'variable_declarator':
                            field_name = field.children[0].text.decode('utf-8')  # 'variable_declarator'节点下标为0的子节点是变量名
                            unused_fields[field_name] = field
            # 遍历类中的方法
            for method in node.children:
                if method.type == 'method_declaration':
                    unused_fields = self.__visit_children(unused_fields, method)
            self.smell = len(unused_fields) > 0
