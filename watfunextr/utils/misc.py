def indent(text: str, lvl: int):
    if not text:
        raise ValueError('Text cannot be empty')
    if lvl < 1:
        raise ValueError('Level of indentation cannot be less than one')
    indentation: str = '\t'*lvl
    return indentation + text.replace('\n', '\n' + indentation)
