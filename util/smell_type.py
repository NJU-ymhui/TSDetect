from enum import Enum


# 定义一个枚举类SmellType，用于表示各种测试代码异味类型
class SmellType(Enum):
    ASSERTION_ROULETTE = 1,  # 断言轮盘：测试用例中有过多的断言，导致难以确定测试失败的具体原因
    CONDITIONAL_TEST = 2,  # 条件测试：测试结果依赖于特定的条件，可能导致测试不稳定
    CONSTRUCTOR_INITIALIZATION = 3,  # 构造函数初始化：测试类的构造函数中包含测试逻辑，可能导致测试用例难以理解和维护
    DEFAULT_TEST = 4,  # 默认测试：测试用例没有执行任何有意义的测试逻辑
    DUPLICATE_ASSERT = 5,  # 重复断言：测试用例中包含重复的断言逻辑
    EMPTY_TEST = 6,  # 空测试：测试用例中没有包含任何测试逻辑
    EAGER_TEST = 7,  # 过早测试：测试用例在被测试代码完成之前就进行了测试
    EXCEPTION_HANDLING = 8,  # 异常处理：测试用例中不正确地处理了异常
    GENERAL_FIXTURE = 9,  # 通用fixture：测试用例使用了不特定于其测试需求的fixture
    IGNORED_TEST = 10,  # 忽略测试：测试用例被无理由地忽略
    LAZY_TEST = 11,  # 懒测试：测试用例没有充分测试被测试代码的功能
    MAGIC_NUMBER = 12,  # 魔术数字：测试用例中使用了未经解释的魔术数字
    MYSTERY_GUEST = 13,  # 神秘来客：测试用例依赖于未被明确声明的外部资源
    REDUNDANT_ASSERTION = 14,  # 冗余断言：测试用例中包含不必要的断言
    REDUNDANT_PRINT = 15,  # 冗余打印：测试用例中使用了不必要的打印语句
    RESOURCE_OPTIMISM = 16,  # 资源乐观：测试用例没有正确管理资源
    SENSITIVE_EQUALITY = 17,  # 敏感等同：测试用例在比较对象时没有考虑敏感信息
    SLEEPY_TEST = 18,  # 嗜睡测试：测试用例中使用了不稳定的延时方法来同步执行
    UNKNOWN_TEST = 19,  # 未知测试：测试用例没有明确的测试目的
    VERBOSE_TEST = 20  # 冗长测试：测试用例包含过多的输出信息
