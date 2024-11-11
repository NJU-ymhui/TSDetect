from abc import ABC, abstractmethod


# 定义一个探测类接口
class Inspection(ABC):
    def __init__(self):
        self.smell = False

    @abstractmethod
    def get_smell_type(self):
        """
        测试异常味道类型
        :return: SmellType
        """
        pass

    @abstractmethod
    def has_smell(self):
        """是否有测试坏味道"""
        pass

    @abstractmethod
    def visit(self, node):
        """访问某个节点"""
        pass

    def clean(self):
        """清除smell状态"""
        self.smell = False

    def logs_info(self):
        return False


