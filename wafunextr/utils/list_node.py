from wafunextr.utils.node import Node


class ListNode(Node):
    def __init__(self, line: int, col: int, name: str = 'List', *children: Node):
        if line < 1:
            raise ValueError('Line cannot be less than one')
        if col < 1:
            raise ValueError('Column cannot be less than one')
        self.name = name
        self.children = [child for child in children]
        self.line = line
        self.col = col

    def __repr__(self):
        return f'({self.name}, [{", ".join(str(child) for child in self.children)}], {self.line}:{self.col})'

    def add_child(self, child: Node):
        if child is None:
            raise ValueError('Child cannot be None')
        self.children.append(child)

    def __eq__(self, other):
        if isinstance(other, ListNode):
            return (self.name, self.children, self.line, self.col) == (other.name, other.children, self.line, self.col)
        raise NotImplemented
