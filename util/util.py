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


def is_print(bs, language='java'):
    if language == 'java':
        return bs.startswith(b'System.out.print') or bs.startswith(b'System.out.println') or \
            bs.startswith(b'System.err.print') or bs.startswith(b'System.err.println')
    elif language == 'go':
        return bs in [b'fmt.Println', b'fmt.Print', b'fmt.Sprintf', b'fmt.Fprintf', b'fmt.Printf']


def get_class_name(node):
    if node.type != 'class_declaration':
        return None
    return node.child_by_field_name('name').text


def is_test_class(name):
    return b'test' in name or b'Test' in name


def is_test_func(method_decl_node):
    pattern1 = r'.*[Tt][Ee][Ss][Tt]'
    pattern2 = r'[Tt][Ee][Ss][Tt].*'
    if method_decl_node.type != 'function_declaration':
        return False
    for child in method_decl_node.children:
        if child.type == 'identifier':
            # function_declaration的子节点的identifier是函数名
            if re.search(pattern1, str(child.text)) or re.search(pattern2, str(child.text)):
                return True
            else:
                return False
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


def count_statements(method, language='java'):
    if language == 'java':
        if method.text == b';':
            return 1
        cnt = 0
        for child in method.children:
            cnt += count_statements(child)
        return cnt
    elif language == 'go':
        block = get_method_body(method, 'go')
        if block is None:
            return 0
        return __count_statements_helper(block)


def __count_statements_helper(block):
    cnt = 0
    if block.type == 'block':
        for child in block.children:
            if child.type not in ['{', '}', 'comment', 'block']:  # 空block不算一个语句
                cnt += 1

    for child in block.children:
        cnt += __count_statements_helper(child)
    return cnt


def is_method_decl(node, language='java'):
    if language == 'java':
        return node.type == 'method_declaration'
    elif language == 'go':
        return node.type == 'function_declaration'


def ignore_annotation(bs):
    s = str(bs)
    ignore = r'(.*)[Ii][Gg][Nn][Oo][Rr][Ee][Dd](.*)'
    disabled = r'(.*)[Dd][Ii][Ss][Aa][Bb][Ll][Ee][Dd](.*)'
    return re.search(ignore, s) or re.search(disabled, s)


def is_global_var(node):
    # for go
    parent = node.parent
    return parent.type == 'source_file'
