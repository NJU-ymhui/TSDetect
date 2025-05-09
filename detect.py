import sys
from datetime import datetime

from tree_sitter import Language, Parser
from visitor.tree_visitor import TreeVisitor
from inspection_manager.inspection_manager import InspectionManager
from inspections.python.assertion_roulette_inspection import AssertionRouletteInspection
from inspections.python.conditional_test_logic_inspection import ConditionalTestLogicInspection
from inspections.python.constructor_initialization_inspection import ConstructorInitializationInspection
from inspections.python.default_test_inspection import DefaultTestInspection
from inspections.python.duplicate_assert_inspection import DuplicateAssertInspection
from inspections.python.eager_test_inspection import EagerTestInspection
from inspections.python.empty_method_inspection import EmptyMethodInspection
from inspections.python.exception_handling_inspection import ExceptionHandlingInspection
from inspections.python.general_fixture_inspection import GeneralFixtureInspection
from inspections.python.test_run_war_inspection import TestRunWarInspection
from inspections.python.ignored_test_inspection import IgnoredTestInspection
from inspections.python.verbose_variable_inspection import VerboseVariableInspection
from inspections.python.lazy_test_inspection import LazyTestInspection
from inspections.python.magic_number_inspection import MagicNumberInspection
from inspections.python.mystery_guest_inspection import MysteryGuestInspection
from inspections.python.redundant_assertion_inspection import RedundantAssertionInspection
from inspections.python.redundant_print_inspection import RedundantPrintInspection
from inspections.python.resource_optimism_inspection import ResourceOptimismInspection
from inspections.python.sensitive_equality_inspection import SensitiveEqualityInspection
from inspections.python.sleepy_test_inspection import SleepyTestInspection
from inspections.python.unknown_test_inspection import UnknownTestInspection
from inspections.python.verbose_test_inspection import VerboseTestInspection
import os


src = ''
smell_types_freq = {
    'SmellType.ASSERTION_ROULETTE': 0,
    'SmellType.CONDITIONAL_TEST': 0,
    'SmellType.CONSTRUCTOR_INITIALIZATION': 0,
    'SmellType.DEFAULT_TEST': 0,
    'SmellType.DUPLICATE_ASSERT': 0,
    'SmellType.EAGER_TEST': 0,
    'SmellType.EMPTY_TEST': 0,
    'SmellType.EXCEPTION_HANDLING': 0,
    'SmellType.GENERAL_FIXTURE': 0,
    'SmellType.IGNORED_TEST': 0,
    'SmellType.LAZY_TEST': 0,
    'SmellType.MAGIC_NUMBER': 0,
    'SmellType.MYSTERY_GUEST': 0,
    'SmellType.REDUNDANT_ASSERTION': 0,
    'SmellType.REDUNDANT_PRINT': 0,
    'SmellType.RESOURCE_OPTIMISM': 0,
    'SmellType.SENSITIVE_EQUALITY': 0,
    'SmellType.SLEEPY_TEST': 0,
    'SmellType.UNKNOWN_TEST': 0,
    'SmellType.VERBOSE_TEST': 0,
    'SmellType.TATE_LEAKAGE': 0,
    'SmellType.TEST_RUN_WAR': 0,
    'SmellType.VERBOSE_VARIABLE': 0,
    'SmellType.NON_DETERMINISTIC_TEST': 0,
    'SmellType.MISSING_CLEANUP': 0,
    'SmellType.LOGS_EXISTS': 0
}


def get_parser():
    parser = Parser()
    Language.build_library(
        'build/my-languages.so',
        [
            'tree-sitter-python'
        ]
    )
    python_language = Language('build/my-languages.so', 'python')
    parser.set_language(python_language)
    return parser


def get_tree(parser, code):
    return parser.parse(code)


def generate_code(path):
    with open(path, 'rb') as file:
        code = file.read()  # 读取整个文件内容
    return code


def register_for(inspection_manager):
    # 尝试解析源代码文件路径, 获得根节点
    src_root = None
    if src != '' and os.path.exists(src):
        # print(src)
        code = generate_code(src)
        parser = get_parser()
        tree = get_tree(parser, code)
        src_root = tree.root_node

    assertion_roulette_inspection = AssertionRouletteInspection()
    conditional_test_logic_inspection = ConditionalTestLogicInspection()
    constructor_initialization_inspection = ConstructorInitializationInspection()
    default_test_inspection = DefaultTestInspection()
    duplicate_assert_inspection = DuplicateAssertInspection()
    eager_test_inspection = EagerTestInspection(src_root)
    test_run_war_inspection = TestRunWarInspection()
    empty_method_inspection = EmptyMethodInspection()
    exception_handling_inspection = ExceptionHandlingInspection()
    general_fixture_inspection = GeneralFixtureInspection()
    ignored_test_inspection = IgnoredTestInspection()
    lazy_test_inspection = LazyTestInspection(src_root)
    magic_number_inspection = MagicNumberInspection()
    mystery_guest_inspection = MysteryGuestInspection()
    verbose_variable_inspection = VerboseVariableInspection()
    redundant_assertion_inspection = RedundantAssertionInspection()
    redundant_print_inspection = RedundantPrintInspection()
    resource_optimism_inspection = ResourceOptimismInspection()
    sensitive_equality_inspection = SensitiveEqualityInspection()
    sleepy_test_inspection = SleepyTestInspection()
    unknown_test_inspection = UnknownTestInspection()
    verbose_test_inspection = VerboseTestInspection()

    inspection_manager.register(verbose_variable_inspection)
    inspection_manager.register(assertion_roulette_inspection)
    inspection_manager.register(conditional_test_logic_inspection)
    inspection_manager.register(constructor_initialization_inspection)
    inspection_manager.register(default_test_inspection)
    inspection_manager.register(duplicate_assert_inspection)
    inspection_manager.register(eager_test_inspection)
    inspection_manager.register(test_run_war_inspection)
    inspection_manager.register(empty_method_inspection)
    inspection_manager.register(exception_handling_inspection)
    inspection_manager.register(general_fixture_inspection)
    inspection_manager.register(ignored_test_inspection)
    inspection_manager.register(lazy_test_inspection)
    inspection_manager.register(magic_number_inspection)
    inspection_manager.register(mystery_guest_inspection)
    inspection_manager.register(redundant_assertion_inspection)
    inspection_manager.register(redundant_print_inspection)
    inspection_manager.register(resource_optimism_inspection)
    inspection_manager.register(sensitive_equality_inspection)
    inspection_manager.register(sleepy_test_inspection)
    inspection_manager.register(unknown_test_inspection)
    inspection_manager.register(verbose_test_inspection)


tot_smell, comment_cnt = 0, 0


def parse(path, src_file_path=''):
    global src, tot_smell, comment_cnt, smell_types_freq
    parser = get_parser()
    code = generate_code(path)
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

    if os.path.exists(src_file_path):
        src = src_file_path
    else:
        src = ''

    inspection_manager = InspectionManager()
    register_for(inspection_manager)

    visitor.register(inspection_manager)
    visitor.parse()  # 遍历语法树解析
    # visitor.check_all_types()
    print("smell types in", path, end=":\n")
    print(inspection_manager.get_smells())  # 查看所有smell
    tot_smell += len(inspection_manager.get_smells())
    # print(smell_types_freq[SmellType.UNKNOWN_TEST])
    for st in inspection_manager.get_smells():
        smell_types_freq[st] += 1
    if inspection_manager.has_logs_inspection():
        print("Total of logs in this test file:", inspection_manager.get_logs_num())
    print("Total of line comments in this test file:", visitor.get_comments_cnt())
    comment_cnt += visitor.get_comments_cnt()
    print()


def main(directory, author_test=False):
    global src, tot_smell, comment_cnt
    tot_smell = comment_cnt = 0
    for root, dirs, files in os.walk(directory):
        # print(dirs, files)
        if "author_tests" in dirs and not author_test:
            dirs.remove("author_tests")
        for file in files:
            if file.endswith('.py'):
                mid_dir = root[len(path):]  # 当前文件除去测试代码根路径的中间路径, 测试代码与源代码此值须保持一致
                src_file_path = src_path + mid_dir + "\\" + file[:-len("_test.py")] + '.py'
                file_path = os.path.join(root, file)
                src = ''
                parse(file_path, src_file_path)  # 开始解析文件
    print("Total of smells:", tot_smell)
    print("Total of line comments:", comment_cnt)


if __name__ == "__main__":
    path = "tests\\resources\\step1\\deepseek\\python"
    src_path = "src\\resources\\step1\\deepseek\\python"
    now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    output_path = "result\\python\\" + now + "_output.txt"
    origin = sys.stdout
    # main(path, True)
    with open(output_path, 'w') as f:
        sys.stdout = f
        print("Start detecting at " + now + ":")
        print()
        main(path, True)
        now = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        print("End detecting at " + now)
        print("Each smell frequency:")
        for smell_type in smell_types_freq:
            print(smell_type, ":", smell_types_freq[smell_type])

    sys.stdout = origin
    print("Detection finished, output file is", output_path)
