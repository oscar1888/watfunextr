from wafunextr.utils.node import Node


class ListNode(Node):
    def __init__(self, line: int, col: int, name: str = 'List', *children: Node):
        super().__init__(line, col)
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
