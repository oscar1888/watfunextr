import unittest

from tests.utils import read
from watfunextr.extractor import extract
from watfunextr.parser import parse
from watfunextr.tokenizer import tokenize
from watfunextr.writer import write_from_module_fields


class Extractor(unittest.TestCase):
    def test_simple_extraction(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/simple_extraction/simple_extraction_input.wat'
            ))), 1)),
            read('extractor_test_cases/simple_extraction/simple_extraction_output.wat')
        )

    def test_simple_extraction_with_valid_name(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/simple_extraction_with_valid_name/simple_extraction_with_valid_name_input.wat'
            ))), '$b')),
            read('extractor_test_cases/simple_extraction_with_valid_name/simple_extraction_with_valid_name_output.wat')
        )

    def test_invalid_name(self):
        with self.assertRaises(ValueError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/invalid_name.wat'))), 'f1')

        self.assertEqual(str(ctx.exception), "Function names must start with $ symbol")

    def test_non_existent_name(self):
        with self.assertRaises(ValueError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/non_existent_name.wat'))), '$b')

        self.assertEqual(str(ctx.exception), "There is no function called $b in the WAT module")

    def test_negative_fun_index(self):
        with self.assertRaises(ValueError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/non_existent_name.wat'))), -2)

        self.assertEqual(str(ctx.exception), "Function indexes start from 0")

    def test_non_existent_fun_index(self):
        with self.assertRaises(ValueError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/non_existent_fun_index.wat'))), 3)

        self.assertEqual(str(ctx.exception), "Function at index 3 does not exist")


if __name__ == '__main__':
    unittest.main()
