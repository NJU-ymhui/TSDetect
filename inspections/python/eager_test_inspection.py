# from inspections.inspection import Inspection
# from util.smell_type import SmellType
#
#
# class EagerTestInspection(Inspection):
#     def __init__(self):
#         super().__init__()
#         self.__freq = 0  # 生产函数调用次数
#         self.__decls = []
#         self.__calls = []  # 加入前判断是否在decls里，确定是否为生产方法调用
#
#     def get_smell_type(self):
#         return SmellType.EAGER_TEST
#
#     def has_smell(self):
#         return self.smell
#
#     def visit(self, node):
#         if self.smell:
#             return
#         if node.type == 'function_definition':
#             # 获取函数名
#             method_name_node = node.child_by_field_name('name')
#             method_name = method_name_node.text.decode('utf-8')  # 将字节转换为字符串
#             # TODO 需要考虑Python中函数重载的情况
#             if method_name in self.__calls:
#                 self.__freq += 1
#                 if self.__freq > 1:
#                     self.smell = True
#                     return
#             self.__decls.append(method_name)
#         elif node.type == 'call':
#             func_name_node = node.child_by_field_name('function')
#             func_name = func_name_node.text.decode('utf-8')  # 将字节转换为字符串
#             if func_name in self.__decls:
#                 self.__freq += 1
#                 if self.__freq > 1:
#                     self.smell = True
#                     return
#             self.__calls.append(func_name)
#         return
#


from inspections.inspection import Inspection
from util.smell_type import SmellType
from util.python.util import is_test_func


class EagerTestInspection(Inspection):
    # 已finish: 有一个问题:Java支持先使用后声明, 这导致当你先调用一个candidate但是在这之后candidate才被声明,那么在调用的时候是不知道它可能引入smell
    # 考虑用回调的方法或者回头看的方法解决
    # 一个测试函数应当只测试一个待测方法，可以多次调用这个待测方法，但只能有一种待测方法
    # 不必考虑java overloading, 认为是同一种方法, 因为没有数据流分析不好区分
    def __init__(self, src_root=None):
        super().__init__()
        self.__eager_candidates = []  # 可能引入smell的非测试方法
        self.__variables_of_tested_class = []  # 只考虑局部变量，不考虑全局变量
        self.__cur_tested = b''  # 当前测试方法测试的待测方法
        self.__method_decl_name = b''  # 测试类中声明的方法名
        self.__class_tobe_tested = b''  # 待测类名
        self.__methods_tobe_tested = []  # 待测类中的待测方法
        self.__non_test_table = []  # 非测试方法的函数名
        self.__use_of_not_decl = []  # 元素是元组，第一位为caller第二位是callee，若caller是测试方法则恒为"@test", 反之是方法名
        self.__is_test = True
        class_body = None
        if src_root is not None:
            for child in src_root.children:
                if child.type == 'class_definition':
                    for child_child in child.children:
                        if child_child.type == 'identifier':
                            self.__class_tobe_tested = child_child.text
                        if child_child.type == 'block':
                            class_body = child_child
                            break
                    break
                if child.type == 'function_definition':
                    for child_child in child.children:
                        if child_child.type == 'identifier':
                            name = child_child.text
                            self.__methods_tobe_tested.append(name)
                            break
                    # break  理论上我们的实验不会出现多个函数声明的源代码（抽取过），但为了泛用性还是注释掉break
            if class_body is not None:
                for child in class_body.children:
                    if child.type == 'function_definition':
                        for method in child.children:
                            if method.type == 'identifier':
                                name = method.text
                                self.__methods_tobe_tested.append(name)

    def get_smell_type(self):
        return SmellType.EAGER_TEST

    def has_smell(self):
        return self.smell

    def visit(self, node):
        if self.smell:
            return
        if node.type == 'function_definition':  # 可能会进入一个测试方法的声明
            self.__is_test = is_test_func(node)
            self.__variables_of_tested_class = []
            self.__cur_tested = b''
            for child in node.children:
                if child.type == 'identifier':
                    self.__method_decl_name = child.text
            if not self.__is_test:
                self.__non_test_table.append(self.__method_decl_name)  # 注册一个非测试方法, 且代表目前它已经声明
        # elif node.type == 'local_variable_declaration':
        #     ty = node.children[0].text
        #     if ty == self.__class_tobe_tested:
        #         for child in node.children:
        #             if child.type == 'variable_declarator':
        #                 # 下标0是变量名
        #                 var_name = child.children[0].text
        #                 self.__variables_of_tested_class.append(var_name)
        elif node.type == 'call':
            var_name = node.children[0].text  # 0号节点要么是func如果是func(), 要么是变量名var如果是var.method()
            method_name = ''
            if var_name not in self.__non_test_table:  # 不过python应该不用担心，不能先使用再声明
                # 如果名字都不在已声明的非测试方法中，那必然不可能在candidates中
                # 记录以在之后声明时回调
                # 下面要验证是不是func(), 即没有.
                if str(var_name).find('.') == -1:
                    # 确实是func()形式的调用，且尚未声明
                    cur_name = self.__method_decl_name
                    if self.__is_test:
                        cur_name = '@test'
                    # 记录
                    self.__use_of_not_decl.append((cur_name, var_name))
            if var_name in self.__eager_candidates:  # 若是func()且匹配候选则触发smell(因为in candidates的一定是func())
                if self.__is_test:
                    self.smell = True
                    return
                self.__eager_candidates.append(self.__method_decl_name)
                return
            # 提取第一组变量名和方法名, 若v.a().b().c()..., 不管了
            for i in range(len(node.children)):
                if node.children[i].type == '.':
                    # var_name = node.children[i - 1].text
                    method_name = node.children[i + 1].text
                    break
            if method_name == '':
                method_name = var_name  # 没有'.'
            if method_name in self.__methods_tobe_tested:
                # print(method_name, self.__methods_tobe_tested)
                # 是待测类的一个变量, 下面检验该变量调用的方法是否和当前测试的方法一致
                if self.__cur_tested == b'':
                    # 还没识别到待测方法
                    self.__cur_tested = method_name
                elif self.__cur_tested != method_name:
                    # 调用的测试方法和之前测的不一致, 说明测试了多个待测方法, 需要触发smell
                    if self.__is_test:
                        self.smell = True
                        return
                    else:  # 下面写不写应该都行，python不像Java可以后向声明
                        # 回调__use_of_not_decl来查看是否有存在先使用再声明的情况，若有，回调更新状态
                        for item in self.__use_of_not_decl:
                            if item[0] == '@test' and item[1] == self.__method_decl_name:
                                # 之前有某个测试方法调用了当前这个非测试方法，但是当时没有声明
                                # 而这个测试方法使用的非测试方法在后续的定义过程中引入了smell，因此触发
                                self.smell = True
                                return
                            elif item[1] == self.__method_decl_name:
                                # 之前调用当前这个引入smell的是非测试方法，则将它加入候选
                                self.__eager_candidates.append(item[0])
                    self.__eager_candidates.append(self.__method_decl_name)
                    return

