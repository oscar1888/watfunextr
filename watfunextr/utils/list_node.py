from watfunextr.utils.node import Node


class ListNode(Node):
    def __init__(self, start_line: int, start_col: int, end_line: int = None, end_col: int = None, name: str = 'List', *children: Node):
        super().__init__(start_line, start_col)
        self.name = name
        self.children = [child for child in children]
        if end_line < 1:
            raise ValueError('End line cannot be less than 1')
        if end_col < 1:
            raise ValueError('End column cannot be less than 1')
        self.end_line = end_line
        self.end_col = end_col

    def __repr__(self):
        return f'({self.name}, [{", ".join(str(child) for child in self.children)}], {self.line}:{self.col}, {self.end_line}:{self.end_col})'

    def add_child(self, child: Node):
        if child is None:
            raise ValueError('Child cannot be None')
        self.children.append(child)

    def __eq__(self, other):
        if isinstance(other, ListNode):
            return ((self.name, self.children, self.line, self.col, self.end_line, self.end_col)
                    == (other.name, other.children, other.line, other.col, other.end_line, other.end_col))
        raise NotImplemented

    def __hash__(self):
        return hash((self.name, self.children, self.line, self.col, self.end_line, self.end_col))
