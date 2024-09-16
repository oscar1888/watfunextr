from wafunextr.utils.node import Node


class ListNode(Node):
    def __init__(self, name: str = 'List', *children: Node):
        self.name = name
        self.children = [child for child in children] if children is not None else []

    def __repr__(self):
        return f'({self.name}, [{", ".join(str(child) for child in self.children)}])'

    def add_child(self, child: Node):
        if child is None:
            raise ValueError('Child cannot be None')
        self.children.append(child)

    def __eq__(self, other):
        if isinstance(other, ListNode):
            return (self.name, self.children) == (other.name, other.children)
        raise NotImplemented
