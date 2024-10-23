import re


def get_method_body(node, language="java"):
    """
    获取方法的代码体部分
    :param node: 方法节点
    :param language: 待测语言
    :return: 方法block
    """
    if language == "java":
        if node.type != 'method_declaration':
            return None
        i = 0
        block = node.children[i]
        while block.type != 'block' and i < len(node.children):
            block = node.children[i]
            i += 1
        if block.type == ';':
            # 说明这是一个带异常声明的函数声明，想要找到它的block需要从父节点开始
            parent = node.parent
            for candidate in parent.children:
                if candidate.type == 'block':
                    block = candidate
                    return block
        elif block.type != 'block':
            return None
        return block
    elif language == 'go':
        if node.type != 'function_declaration':
            return None
        for i, child in enumerate(node.children):
            if child.type == 'block':
                return child
        return None


def is_number(bs):
    for b in bs:
        if not ord('0') <= b <= ord('9'):
            return False
    return True


def index_of(node, key):
    """找子节点中text内容为key的"""
    for i, child in enumerate(node.children):
        if child.text == key:
            return i
    return -1


def get_class_body(node):
    if node.type != 'class_declaration':
        print("Error when get a non-class's body")
        return None
    for child in node.children:
        if child.type == 'class_body':
            return child
    print("No body in class", node)
    return None


def is_bool(bs):
    return bs == b'true' or bs == b'false' or bs == b'null'


def is_print(bs):
    return bs.startswith(b'System.out.print') or bs.startswith(b'System.out.println') or \
            bs.startswith(b'System.err.print') or bs.startswith(b'System.err.println')


def get_class_name(node):
    if node.type != 'class_declaration':
        return None
    return node.child_by_field_name('name').text


def is_test_class(name):
    return b'test' in name or b'Test' in name


def is_test_func(method_decl_node):
    if method_decl_node.type != 'method_declaration':
        return False
    for child in method_decl_node.children:
        if child.type == 'modifiers':
            # 看注解中是否包含test
            for c in child.children:
                if c.type == 'marker_annotation':
                    return b'test' in child.text or b'Test' in child.text
    return False


def is_variable_decl(node):
    ty = node.type
    return ty == 'formal_parameter' or ty == 'field_declaration' or ty == 'local_variable_declaration'


def print_child(node):
    children = []
    print(node.text)
    print(node.type, "children: ", end="")
    for child in node.children:
        print(child.text, end=" ")
        children.append(child)
    if len(children) == 0:
        return
    print()
    for child in children:
        if len(child.children) == 0:
            continue
        print_child(child)


def count_statements(method):
    if method.text == b';':
        return 1
    cnt = 0
    for child in method.children:
        cnt += count_statements(child)
    return cnt


def is_method_decl(node):
    return node.type == 'method_declaration'


def ignore_annotation(bs):
    s = str(bs)
    ignore = r'(.*)[Ii][Gg][Nn][Oo][Rr][Ee][Dd](.*)'
    disabled = r'(.*)[Dd][Ii][Ss][Aa][Bb][Ll][Ee][Dd](.*)'
    return re.search(ignore, s) or re.search(disabled, s)
