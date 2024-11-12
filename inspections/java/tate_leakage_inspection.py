from util.smell_type import SmellType
from inspections.inspection import Inspection
from util.java.util import get_method_body


class TateLeakageInspection(Inspection):
    def __init__(self):
        super().__init__()
        self.__global_vars = []

    def get_smell_type(self):
        return SmellType.TATE_LEAKAGE

    def has_smell(self):
        return len(self.__global_vars) > 0

    def __visit_block(self, block):
        for child in block.children:
            if child.type == 'assignment_expression':
                # 赋值表达式, 下标0是左值
                l_val = child.children[0].text
                if l_val in self.__global_vars:
                    self.__global_vars.remove(l_val)
            self.__visit_block(child)

    def visit(self, node):
        # 使用全局变量且并不是都在setup里初始化，并且有不止一个测试方法
        if node.type == 'field_declaration':
            for child in node.children:
                if child.type == 'variable_declarator':
                    # 下标0是变量名
                    var_name = child.children[0].text
                    self.__global_vars.append(var_name)
        elif node.type == 'method_declaration':
            # 这一坨意在检查是不是setup方法，如果是，访问其中初始化的变量
            setup = False
            for child in node.children:
                if child.type == 'modifiers':
                    # 有没有访问控制说明
                    for anno in child.children:
                        # 有没有注解及是不是@Before
                        if anno.type == 'marker_annotation' and anno.text == b'@Before':
                            setup = True
                if setup and child.type == 'identifier' and child.text == b'setUp':
                    block = get_method_body(node)
                    self.__visit_block(block)
                    return

