from typing import Tuple


class ExtractionError(Exception):
	def __init__(self, msg: str, line_col: Tuple[int, int] = None):
		if line_col is not None:
			msg = f'Extraction error at {line_col[0]}:{line_col[1]}: {msg}'
		else:
			msg = f'Extraction error: {msg}'
		super().__init__(msg)
