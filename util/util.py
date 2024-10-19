def get_method_body(node):
    """
    获取方法的代码体部分
    :param node: 方法节点
    :return: 方法block
    """
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

