class Node:
    def __init__(self, line: int, col: int):
        if line < 1:
            raise ValueError('Line cannot be less than one')
        if col < 1:
            raise ValueError('Column cannot be less than one')
        self.line = line
        self.col = col
