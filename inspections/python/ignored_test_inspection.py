from inspections.inspection import Inspection
from util.smell_type import SmellType


class IgnoredTestInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.IGNORED_TEST

    def has_smell(self):
        return self.smell

    #
    # def visit(self, node):
    #     # 获取该方法的注解，检查是否包含 @Ignore 或 @Disabled 注解。
    #     # 如果发现这些注解，返回 true，表示存在“气味”。
    #     if self.smell:
    #         return
    #     if node.type == 'marker_annotation' or node.type == 'normal_annotation' or node.type == 'annotation':
    #         text = node.text
    #         if text == b'@Ignore' or text == b'@Disabled':
    #             self.smell = True
    #             return
    #         return
    #     return
    # def visit(self, node):
    #     # 获取该方法的装饰器，检查是否包含 @ignore 或 @disabled 装饰器。
    #     if self.smell:
    #         return
    #     if node.type == 'decorator':
    #         # print(f"%%%%%%%%%%%%%%%%node:{node.child_by_field_name('name')}")
    #         # decorator_name = node.child_by_field_name('name').text.decode('utf-8')
    #         # if decorator_name == 'ignore' or decorator_name == 'disabled':
    #         if node.child_by_field_name('name'):
    #             decorator_name = node.child_by_field_name('name').text.decode('utf-8').lower()
    #             if 'ignore' in decorator_name or 'disabled' in decorator_name or 'skip' in decorator_name:
    #                 self.smell = True
    #                 return
    #     for child in node.children:
    #         self.visit(child)
    def visit(self, node):
        # 获取该方法的装饰器，检查是否包含 @ignore 或 @disabled 装饰器。
        if self.smell:
            return
        if node.type == 'decorated_definition':
            for decorator in node.children[0].children:
                if decorator.type == 'decorator':
                    decorator_name = decorator.child_by_field_name('name').text.decode('utf-8').lower()
                    if 'ignore' in decorator_name or 'disabled' in decorator_name or 'skip' in decorator_name:
                        self.smell = True
                        return
        for child in node.children:
            self.visit(child)
