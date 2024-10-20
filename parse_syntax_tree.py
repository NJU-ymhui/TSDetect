from tree_sitter import Language, Parser
from visitor.tree_visitor import TreeVisitor
from inspection_manager.inspection_manager import InspectionManager
from inspections.assertion_roulette_inspection import AssertionRouletteInspection
from inspections.conditional_test_logic_inspection import ConditionalTestLogicInspection
from inspections.constructor_initialization_inspection import ConstructorInitializationInspection
from inspections.default_test_inspection import DefaultTestInspection
from inspections.duplicate_assert_inspection import DuplicateAssertInspection
from inspections.eager_test_inspection import EagerTestInspection
from inspections.empty_method_inspection import EmptyMethodInspection
from inspections.exception_handling_inspection import ExceptionHandlingInspection
from inspections.general_fixture_inspection import GeneralFixtureInspection
from inspections.ignored_test_inspection import IgnoredTestInspection
from inspections.lazy_test_inspection import LazyTestInspection
from inspections.magic_number_inspection import MagicNumberInspection
from inspections.mystery_guest_inspection import MysteryGuestInspection
from inspections.redundant_assertion_inspection import RedundantAssertionInspection
from inspections.redundant_print_inspection import RedundantPrintInspection
from inspections.resource_optimism_inspection import ResourceOptimismInspection
from inspections.sensitive_equality_inspection import SensitiveEqualityInspection
from inspections.sleepy_test_inspection import SleepyTestInspection
from inspections.unknown_test_inspection import UnknownTestInspection
from inspections.verbose_test_inspection import VerboseTestInspection


def get_parser():
    parser = Parser()
    Language.build_library(
        'build/my-languages.so',
        [
            'tree-sitter-java'
        ]
    )
    java_language = Language('build/my-languages.so', 'java')
    parser.set_language(java_language)
    return parser


def get_tree(parser, code):
    return parser.parse(code)


def generate_code(path):
    with open(path, 'rb') as file:
        code = file.read()  # 读取整个文件内容
    return code


if __name__ == "__main__":
    parser = get_parser()
    code = generate_code("E:\\LLM4SE\\ISSTA\\data\\java\\TSDetect\\tests\\resources\\redundant_assert.java")
    tree = get_tree(parser, code)
    visitor = TreeVisitor(tree.root_node)
    print("types:")
    visitor.check_all_types()
    # print("calls:")
    # visitor.check_method_call()
    # print("decls:")
    # visitor.check_method_decl()
    # print("statements:")
    # visitor.print_statements_from_root()

    inspection_manager = InspectionManager()
    assertion_roulette_inspection = AssertionRouletteInspection()
    conditional_test_logic_inspection = ConditionalTestLogicInspection()
    constructor_initialization_inspection = ConstructorInitializationInspection()
    default_test_inspection = DefaultTestInspection()
    duplicate_assert_inspection = DuplicateAssertInspection()
    eager_test_inspection = EagerTestInspection()
    empty_method_inspection = EmptyMethodInspection()
    exception_handling_inspection = ExceptionHandlingInspection()
    general_fixture_inspection = GeneralFixtureInspection()
    ignored_test_inspection = IgnoredTestInspection()
    lazy_test_inspection = LazyTestInspection()
    magic_number_inspection = MagicNumberInspection()
    mystery_guest_inspection = MysteryGuestInspection()
    redundant_assertion_inspection = RedundantAssertionInspection()
    redundant_print_inspection = RedundantPrintInspection()
    resource_optimism_inspection = ResourceOptimismInspection()
    sensitive_equality_inspection = SensitiveEqualityInspection()
    sleepy_test_inspection = SleepyTestInspection()
    unknown_test_inspection = UnknownTestInspection()
    verbose_test_inspection = VerboseTestInspection()

    inspection_manager.register(assertion_roulette_inspection)
    inspection_manager.register(conditional_test_logic_inspection)
    inspection_manager.register(constructor_initialization_inspection)
    inspection_manager.register(default_test_inspection)
    inspection_manager.register(duplicate_assert_inspection)
    inspection_manager.register(eager_test_inspection)
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

    visitor.register(inspection_manager)
    visitor.parse()  # 遍历语法树解析
    print(inspection_manager.get_smells())  # 查看所有smell
