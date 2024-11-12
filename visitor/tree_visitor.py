class TreeVisitor:
    def __init__(self, root):
        self.__root = root
        self.__inspection_manager = None
        self.__comments_cnt = 0  # visitor统计行注释数量

    def __print_statements_helper(self, node):
        for child in node.children:
            if child.type == 'expression_statement':
                print(child.text)
            self.__print_statements_helper(child)

    def print_statements_from_root(self):
        self.__print_statements_helper(self.__root)

    def __check_method_call_helper(self, node):
        for child in node.children:
            if child.type == 'method_invocation':
                print("!!!!!!")
                print(child.children[1].text)
                print("!!!!!!")
            self.__check_method_call_helper(child)

    def check_method_call(self):
        return self.__check_method_call_helper(self.__root)

    def __check_method_decl_helper(self, node):
        for child in node.children:
            if child.type == 'method_declaration':
                print("------")
                print(child.children[2].text)
                print("------")
            self.__check_method_decl_helper(child)

    def check_method_decl(self):
        return self.__check_method_decl_helper(self.__root)

    def __check_all_types_helper(self, node):
        for child in node.children:
            if child.type == 'variable_declarator':
                print("------", child.parent.children[0].text, "------")
            print(child.type + ":", child.text)
            self.__check_all_types_helper(child)

    def check_all_types(self):
        print("root:", self.__root.type)
        return self.__check_all_types_helper(self.__root)

    def register(self, manager):
        # 请务必在self.parse()之前调用
        self.__inspection_manager = manager

    def __parse_helper(self, node):
        for child in node.children:
            if child.type == 'line_comment' or child.type == 'comment':
                self.__comments_cnt += 1
                continue
            self.__inspection_manager.visit(child)
            self.__parse_helper(child)

    def parse(self):
        """
        遍历整棵语法树
        """
        if self.__inspection_manager is None:
            print("Error!")
            raise Exception("Please register an inspection manager before parsing")
        self.__comments_cnt = 0
        self.__parse_helper(self.__root)

    def get_comments_cnt(self):
        return self.__comments_cnt
