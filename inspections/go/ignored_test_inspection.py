from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.go.util import ignore_annotation


class IgnoredTestInspection(Inspection):
    def __init__(self):
        super().__init__()

    def get_smell_type(self):
        return SmellType.IGNORED_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        # 获取该方法的注解，检查是否包含 @Ignore 或 @Disabled 注解。
        # 如果发现这些注解，返回 true，表示存在“气味”。
        if self.smell:
            return
        if node.type == 'marker_annotation' or node.type == 'normal_annotation' or node.type == 'annotation':
            text = node.text
            self.smell = ignore_annotation(text)
            return
        return
