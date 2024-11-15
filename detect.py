from tree_sitter import Language, Parser
from visitor.tree_visitor import TreeVisitor
from inspection_manager.inspection_manager import InspectionManager
from inspections.assertion_roulette_inspection import AssertionRouletteInspection
from inspections.conditional_test_logic_inspection import ConditionalTestLogicInspection
from inspections.default_test_inspection import DefaultTestInspection
from inspections.duplicate_assert_inspection import DuplicateAssertInspection
from inspections.lazy_test_inspection import LazyTestInspection
from inspections.empty_method_inspection import EmptyMethodInspection
from inspections.exception_handling_inspection import ExceptionHandlingInspection
from inspections.general_fixture_inspection import GeneralFixtureInspection
from inspections.eager_test_inspection import EagerTestInspection
from inspections.magic_number_inspection import MagicNumberInspection
from inspections.mystery_guest_inspection import MysteryGuestInspection
from inspections.redundant_print_inspection import RedundantPrintInspection
from inspections.resource_optimism_inspection import ResourceOptimismInspection
from inspections.sleepy_test_inspection import SleepyTestInspection
from inspections.unknown_test_inspection import UnknownTestInspection
from inspections.verbose_test_inspection import VerboseTestInspection
from inspections.logs_inspection import LogsInspection
from inspections.tate_leakage_inspection import TATELeakageInspection
from inspections.test_run_war_inspection import TestRunWarInspection
from inspections.non_deterministic_inspection import NonDeterministicInspection
from inspections.verbose_variable_inspection import VerboseVariableInspection
import os
from datetime import datetime
import sys


def get_parser():
    parser = Parser()
    Language.build_library(
        'build/my-languages.so',
        [
            'tree-sitter-go'
        ]
    )
    java_language = Language('build/my-languages.so', 'go')
    parser.set_language(java_language)
    return parser


def get_tree(parser, code):
    return parser.parse(code)


def generate_code(file_path):
    with open(file_path, 'rb') as file:
        code = file.read()  # 读取整个文件内容
    return code


src = ''


def register_for(inspection_manager):
    # 尝试引入测试源文件，然后解析出根节点，从而初始化eager和lazy
    src_root = None
    if src != '' and os.path.exists(src):
        # 解析源文件得到src_root
        with open(src, 'rb') as sf:
            code = sf.read()
        parser = get_parser()
        tree = parser.parse(code)
        src_root = tree.root_node

    assertion_roulette_inspection = AssertionRouletteInspection()
    conditional_test_logic_inspection = ConditionalTestLogicInspection()
    # constructor_initialization_inspection = ConstructorInitializationInspection()
    default_test_inspection = DefaultTestInspection()
    duplicate_assert_inspection = DuplicateAssertInspection()
    eager_test_inspection = EagerTestInspection(src_file_root=src_root)
    empty_method_inspection = EmptyMethodInspection()
    exception_handling_inspection = ExceptionHandlingInspection()
    general_fixture_inspection = GeneralFixtureInspection()
    # ignored_test_inspection = IgnoredTestInspection()
    lazy_test_inspection = LazyTestInspection(src_file_root=src_root)
    magic_number_inspection = MagicNumberInspection()
    mystery_guest_inspection = MysteryGuestInspection()
    # redundant_assertion_inspection = RedundantAssertionInspection()
    redundant_print_inspection = RedundantPrintInspection()
    resource_optimism_inspection = ResourceOptimismInspection()
    # sensitive_equality_inspection = SensitiveEqualityInspection()
    sleepy_test_inspection = SleepyTestInspection()
    unknown_test_inspection = UnknownTestInspection()
    verbose_test_inspection = VerboseTestInspection()
    logs_inspection = LogsInspection()
    tate_leakage_inspection = TATELeakageInspection()
    test_run_war_inspection = TestRunWarInspection()
    non_deterministic_inspection = NonDeterministicInspection()
    verbose_variable_inspection = VerboseVariableInspection()

    inspection_manager.register(assertion_roulette_inspection)
    inspection_manager.register(conditional_test_logic_inspection)
    # inspection_manager.register(constructor_initialization_inspection)  # go没有构造函数
    inspection_manager.register(default_test_inspection)
    inspection_manager.register(duplicate_assert_inspection)
    inspection_manager.register(eager_test_inspection)
    inspection_manager.register(empty_method_inspection)
    inspection_manager.register(exception_handling_inspection)
    inspection_manager.register(general_fixture_inspection)
    # inspection_manager.register(ignored_test_inspection)  # go没有ignore注解
    inspection_manager.register(lazy_test_inspection)
    inspection_manager.register(magic_number_inspection)
    inspection_manager.register(mystery_guest_inspection)
    # inspection_manager.register(redundant_assertion_inspection)  # go不存在真假值断言的直接概念，自然不能断定其参数一定为布尔值
    inspection_manager.register(redundant_print_inspection)
    inspection_manager.register(resource_optimism_inspection)
    # inspection_manager.register(sensitive_equality_inspection)  # go没有对象有没有toString()方法
    inspection_manager.register(sleepy_test_inspection)
    inspection_manager.register(unknown_test_inspection)
    inspection_manager.register(verbose_test_inspection)
    inspection_manager.register(logs_inspection)
    inspection_manager.register(tate_leakage_inspection)
    inspection_manager.register(test_run_war_inspection)
    inspection_manager.register(non_deterministic_inspection)
    inspection_manager.register(verbose_variable_inspection)


def parse(file_path, src_path=''):
    global src
    parser = get_parser()
    code = generate_code(file_path)
    tree = get_tree(parser, code)
    visitor = TreeVisitor(tree.root_node)
    # print("types:")
    # visitor.check_all_types()
    # print("calls:")
    # visitor.check_method_call()
    # print("decls:")
    # visitor.check_method_decl()
    # print("statements:")
    # visitor.print_statements_from_root()

    inspection_manager = InspectionManager()
    # 做协议规约1，用对拍检查源代码文件是否存在(在main()里)
    if os.path.exists(src_path):
        src = src_path
    else:
        src = ''
    register_for(inspection_manager)

    visitor.register(inspection_manager)
    visitor.parse()  # 遍历语法树解析
    print("smell types in", file_path, end=":\n")
    print(inspection_manager.get_smells())  # 查看所有smell
    if inspection_manager.has_logs_inspection():
        print('Total of logs in this test file:', inspection_manager.get_logs_num())
    print('Total of comments in this test file:', visitor.get_comments_cnt())
    print()


def main(directory, author_test=False):
    global src
    for root, dirs, files in os.walk(directory):
        # print(dirs, files)
        if "author_tests" in dirs and not author_test:
            dirs.remove("author_tests")
        for file in files:
            if file.endswith('.go'):
                file_path = os.path.join(root, file)
                # 判断能不能找到源文件
                # 协议：源（待测）文件放在src里，除去根目录src和最终文件名，中间路径必须一致
                # 先把中间路径截取下来
                mid_dir = root[len(path):]
                # 协议规约2：测试文件名必须是对应源文件名的，去掉后缀，再加_test.go, 对应的，源文件名就是测试文件中_test.go->。go
                src_path = tobe_test_path + mid_dir + "\\" + file[:-8] + '.go'
                src = ''
                parse(file_path, src_path)  # 开始解析文件


if __name__ == "__main__":
    path = "tests\\resources"  # 测试代码位置
    tobe_test_path = "src\\resources"  # 源代码位置
    now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    output_path = "result\\go\\" + now + "_output.txt"
    origin = sys.stdout
    with open(output_path, 'w') as f:
        sys.stdout = f
        print("Start detecting at " + now + ":")
        print()
        main(path)
        now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        print("End detecting at " + now)
    sys.stdout = origin
    print("Detection finished, output file is", output_path)

