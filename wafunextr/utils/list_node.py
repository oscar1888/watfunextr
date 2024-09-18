from wafunextr.utils.node import Node


class ListNode(Node):
    def __init__(self, start_line: int, start_col: int, name: str = 'List', *children: Node):
        super().__init__(start_line, start_col)
        self.name = name
        self.children = [child for child in children]
        self.end_line = None
        self.end_col = None

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
