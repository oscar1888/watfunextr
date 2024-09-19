class Node:
    def __init__(self, start_line: int, start_col: int):
        if start_line < 1:
            raise ValueError('Line cannot be less than one')
        if start_col < 1:
            raise ValueError('Column cannot be less than one')
        self.line = start_line
        self.col = start_col
