from inspections.inspection import Inspection
from util.smell_type import SmellType


class SleepyTestInspection(Inspection):
    # 检测是否使用了 time.sleep 或 asyncio.sleep，可能会导致测试不稳定或耗时过长
    def __init__(self):
        super().__init__()
        self.smell = False
        self.patched_methods = []

    def get_smell_type(self):
        return SmellType.SLEEPY_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return

        if node.type == 'function_definition':
            self.check_decorator(node)

        if node.type == 'call':
            self.check_call(node)

        for child in node.children:
            self.visit(child)

    def check_decorator(self, node):
        # 遍历所有子节点，找到装饰器节点
        for child in node.children:
            decorator_value = child.text.decode('utf-8')
            if 'sleep' in decorator_value:
                self.smell = True
                return


    def check_call(self, node):
        if self.smell:
            return
        function_name = node.child_by_field_name('function')
        if function_name and function_name.type == 'attribute':
            object_name = function_name.child_by_field_name('object')
            method_name = function_name.child_by_field_name('attribute')
            if object_name and method_name:
                object_name_text = object_name.text.decode('utf-8')
                method_name_text = method_name.text.decode('utf-8')
                if (object_name_text in ['time', 'asyncio'] and method_name_text == 'sleep') or (
                        object_name_text in self.patched_methods and method_name_text == 'sleep'):
                    self.smell = True
                    return
