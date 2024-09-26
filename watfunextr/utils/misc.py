def indent(text: str, lvl: int, tab_size: int = 4):
    if not text:
        raise ValueError('Text cannot be empty')
    if lvl < 1:
        raise ValueError('Level of indentation cannot be less than one')
    if tab_size < 1:
        raise ValueError('Tab size cannot be less than one')
    indentation: str = (' '*tab_size)*lvl
    return indentation + text.replace('\n', '\n' + indentation)
