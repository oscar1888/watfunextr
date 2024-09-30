import unittest
from typing import Union

from tests.utils import read
from watfunextr.extractor import extract
from watfunextr.extractor import ExtractionError
from watfunextr.parser import parse
from watfunextr.tokenizer import tokenize
from watfunextr.writer import write_from_module_fields


class Extractor(unittest.TestCase):
    def positive_test(self, test_case_name: str, func_name_or_idx: Union[int, str], output_module: str = None):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                f'extractor_test_cases/{test_case_name}/{test_case_name}_input.wat'
            ))), func_name_or_idx)),
            read(f'extractor_test_cases/{test_case_name}/{test_case_name if output_module is None else output_module}_output.wat')
        )

    def negative_test(self, test_case_name: str, func_name_or_idx: Union[int, str], msg: str):
        with self.assertRaises(ExtractionError) as ctx:
            extract(parse(tokenize(read(f'extractor_test_cases/{test_case_name}.wat'))), func_name_or_idx)

        self.assertEqual(msg, str(ctx.exception))

    def test_simple_extraction(self):
        self.positive_test('simple_extraction', 1)

    def test_simple_extraction_with_valid_name(self):
        self.positive_test('simple_extraction_with_valid_name', '$b')

    def test_invalid_name(self):
        self.negative_test('invalid_name', 'f1', 'Extraction error: Names must start with $ symbol')

    def test_non_existent_name(self):
        self.negative_test('non_existent_name', '$b', 'Extraction error: $b is not a name in the WAT module')

    def test_negative_fun_index(self):
        self.negative_test('non_existent_name', -2, 'Extraction error: Indexes start from 0')

    def test_non_existent_fun_index(self):
        self.negative_test('non_existent_fun_index', 3, 'Extraction error: Index 3 does not exist')

    def test_module_with_illegal_fun_call_idx(self):
        self.negative_test('module_with_illegal_fun_call_idx', '$c', 'Extraction error at 11:14: Index 7 does not exist')

    def test_module_with_illegal_fun_call_name(self):
        self.negative_test('module_with_illegal_fun_call_name', '$c', 'Extraction error at 6:14: $add is not a name in the WAT module')

    def test_one_fun_dependency(self):
        self.positive_test('one_fun_dependency', '$d')

    def test_recursive_fun(self):
        self.positive_test('recursive_fun', '$factorial')

    def test_recursive_fun_with_other_funs(self):
        self.positive_test('recursive_fun_with_other_funs', '$factorial')

    def test_one_recursive_fun_dependency(self):
        self.positive_test('one_recursive_fun_dependency', '$factorial_start')

    def test_recursive_with_in_edge(self):
        self.positive_test('one_recursive_fun_dependency', '$factorial', output_module='recursive_with_in_edge')

    def test_mutually_recursive(self):
        self.positive_test('mutually_recursive', '$is_even')

    def test_mutually_recursive_and_recursive_dep(self):
        self.positive_test('mutually_recursive_and_recursive_dep', '$is_even')

    def test_three_vertex_clique(self):
        self.positive_test('three_vertex_clique', '$f1')

    def test_complex_call_graph(self):
        self.positive_test('complex_call_graph', '$f1')

    def test_three_vertex_clique_with_recursive_dep_input(self):
        self.positive_test('three_vertex_clique_with_recursive_dep', '$f1')

    def test_clique_with_recursion_deps_and_in_edges(self):
        self.positive_test('clique_with_recursion_deps_and_in_edges', '$f1')

    def test_calls_in_expr_section_of_if(self):
        self.positive_test('calls_in_expr_section_of_if', '$is_even')

    def test_calls_in_then_section_of_if(self):
        self.positive_test('calls_in_then_section_of_if', '$is_even')

    def test_calls_in_else_section_of_if(self):
        self.positive_test('calls_in_else_section_of_if', '$is_even')

    def test_calls_in_block(self):
        self.positive_test('calls_in_block', '$f1')

    def test_typedef_dependencies(self):
        self.positive_test('typedef_dependencies', '$is_even')

    def test_global_dependencies(self):
        self.positive_test('global_dependencies', '$doit')


if __name__ == '__main__':
    unittest.main()
