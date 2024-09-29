import unittest

from tests.utils import read
from watfunextr.extractor import extract
from watfunextr.extractor import ExtractionError
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
        with self.assertRaises(ExtractionError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/invalid_name.wat'))), 'f1')

        self.assertEqual(str(ctx.exception), "Names must start with $ symbol")

    def test_non_existent_name(self):
        with self.assertRaises(ExtractionError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/non_existent_name.wat'))), '$b')

        self.assertEqual(str(ctx.exception), "$b is not a name in the WAT module")

    def test_negative_fun_index(self):
        with self.assertRaises(ExtractionError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/non_existent_name.wat'))), -2)

        self.assertEqual(str(ctx.exception), "Indexes start from 0")

    def test_non_existent_fun_index(self):
        with self.assertRaises(ExtractionError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/non_existent_fun_index.wat'))), 3)

        self.assertEqual(str(ctx.exception), "Index 3 does not exist")

    def test_module_with_illegal_fun_call_idx(self):
        with self.assertRaises(ExtractionError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/module_with_illegal_fun_call_idx.wat'))), '$c')

        self.assertEqual(str(ctx.exception), "Extraction error at 11:14: Index 7 does not exist")

    def test_module_with_illegal_fun_call_name(self):
        with self.assertRaises(ExtractionError) as ctx:
            extract(parse(tokenize(read('extractor_test_cases/module_with_illegal_fun_call_name.wat'))), '$c')

        self.assertEqual(str(ctx.exception), "Extraction error at 6:14: $add is not a name in the WAT module")

    def test_one_fun_dependency(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/one_fun_dependency/one_fun_dependency_input.wat'
            ))), '$d')),
            read('extractor_test_cases/one_fun_dependency/one_fun_dependency_output.wat')
        )

    def test_recursive_fun(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/recursive_fun/recursive_fun_input.wat'
            ))), '$factorial')),
            read('extractor_test_cases/recursive_fun/recursive_fun_output.wat')
        )

    def test_recursive_fun_with_other_funs(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/recursive_fun_with_other_funs/recursive_fun_with_other_funs_input.wat'
            ))), '$factorial')),
            read('extractor_test_cases/recursive_fun_with_other_funs/recursive_fun_with_other_funs_output.wat')
        )

    def test_one_recursive_fun_dependency(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/one_recursive_fun_dependency/one_recursive_fun_dependency_input.wat'
            ))), '$factorial_start')),
            read('extractor_test_cases/one_recursive_fun_dependency/one_recursive_fun_dependency_output.wat')
        )

    def test_recursive_with_in_edge(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/one_recursive_fun_dependency/one_recursive_fun_dependency_input.wat'
            ))), '$factorial')),
            read('extractor_test_cases/one_recursive_fun_dependency/recursive_with_in_edge_output.wat')
        )

    def test_mutually_recursive(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/mutually_recursive/mutually_recursive_input.wat'
            ))), '$is_even')),
            read('extractor_test_cases/mutually_recursive/mutually_recursive_output.wat')
        )

    def test_mutually_recursive_and_recursive_dep(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/mutually_recursive_and_recursive_dep/mutually_recursive_and_recursive_dep_input.wat'
            ))), '$is_even')),
            read('extractor_test_cases/mutually_recursive_and_recursive_dep/mutually_recursive_and_recursive_dep_output.wat')
        )

    def test_three_vertex_clique(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/three_vertex_clique/three_vertex_clique_input.wat'
            ))), '$f1')),
            read('extractor_test_cases/three_vertex_clique/three_vertex_clique_output.wat')
        )

    def test_complex_call_graph(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/complex_call_graph/complex_call_graph_input.wat'
            ))), '$f1')),
            read('extractor_test_cases/complex_call_graph/complex_call_graph_output.wat')
        )

    def test_three_vertex_clique_with_recursive_dep_input(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/three_vertex_clique_with_recursive_dep/three_vertex_clique_with_recursive_dep_input.wat'
            ))), '$f1')),
            read('extractor_test_cases/three_vertex_clique_with_recursive_dep/three_vertex_clique_with_recursive_dep_output.wat')
        )

    def test_clique_with_recursion_deps_and_in_edges(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/clique_with_recursion_deps_and_in_edges/clique_with_recursion_deps_and_in_edges_input.wat'
            ))), '$f1')),
            read('extractor_test_cases/clique_with_recursion_deps_and_in_edges/clique_with_recursion_deps_and_in_edges_output.wat')
        )

    def test_calls_in_expr_section_of_if(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/calls_in_expr_section_of_if/calls_in_expr_section_of_if_input.wat'
            ))), '$is_even')),
            read('extractor_test_cases/calls_in_expr_section_of_if/calls_in_expr_section_of_if_output.wat')
        )

    def test_calls_in_then_section_of_if(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/calls_in_then_section_of_if/calls_in_then_section_of_if_input.wat'
            ))), '$is_even')),
            read('extractor_test_cases/calls_in_then_section_of_if/calls_in_then_section_of_if_output.wat')
        )

    def test_calls_in_else_section_of_if(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/calls_in_else_section_of_if/calls_in_else_section_of_if_input.wat'
            ))), '$is_even')),
            read('extractor_test_cases/calls_in_else_section_of_if/calls_in_else_section_of_if_output.wat')
        )

    def test_calls_in_block(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/calls_in_block/calls_in_block_input.wat'
            ))), '$f1')),
            read('extractor_test_cases/calls_in_block/calls_in_block_output.wat')
        )

    def test_typedef_dependencies(self):
        self.assertEqual(
            write_from_module_fields(extract(parse(tokenize(read(
                'extractor_test_cases/typedef_dependencies/typedef_dependencies_input.wat'
            ))), '$is_even')),
            read('extractor_test_cases/typedef_dependencies/typedef_dependencies_output.wat')
        )


if __name__ == '__main__':
    unittest.main()
