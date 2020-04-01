"""
Unit tests for megago.

Usage: python -m unittest -v megago_test
"""

import matplotlib
import unittest
from io import StringIO
# pylint: disable=no-name-in-module
from megago.megago import read_input, is_go_term, plot_similarity


class TestIsStringContaingGo(unittest.TestCase):
    """Unit tests for is_str_containing_go_term"""

    def do_test(self, input_str, expected):
        result = is_go_term(input_str)
        self.assertEqual(expected, result)

    def test_plain_go_string(self):
        expected = True
        self.do_test("GO:0005488", expected)

    def test_non_go_string(self):
        expected = False
        self.do_test("wasd", expected)

    def test_lower_case_go_string(self):
        expected = True
        self.do_test("go:0005488", expected)

    def test_short_too_short_go_string(self):
        expected = False
        self.do_test("go:000588", expected)

    def test_short_too_long_go_string(self):
        expected = False
        self.do_test("go:00058890", expected)

    def test_multiple_go_terms(self):
        expected = False
        self.do_test("GO:1234567;GO:1234568", expected)


class TestReadInput(unittest.TestCase):
    '''Unit tests for read_input'''

    def do_test(self, input_str, expected):
        "Wrapper function for testing read_input"
        result = read_input(StringIO(input_str))
        self.assertEqual(expected, result)

    def test_zero_byte_input(self):
        "Test input containing zero bytes"
        expected = [], [], []
        self.do_test('', expected)

    def test_valid_go_terms(self):
        string = """id1,GO:0005488,GO:0048037;GO:0036094
id2,GO:0098581,GO:0032490;GO:0098543
id3,GO:0050789,GO:0030155;GO:0031341"""
        expected = (["id1", "id2", "id3"],
                    [['GO:0005488'], ['GO:0098581'], ['GO:0050789']],
                    [['GO:0048037', 'GO:0036094'],
                     ['GO:0032490', 'GO:0098543'],
                     ['GO:0030155', 'GO:0031341']])
        self.do_test(string, expected)

    def test_second_tool_no_go_terms(self):
        string = """id1,GO:0098581,
id2,GO:0050789,GO:0030155;GO:0031341"""
        expected = (["id1", "id2"],
                    [['GO:0098581'], ['GO:0050789']],
                    [[], ['GO:0030155', 'GO:0031341']])
        self.do_test(string, expected)

    def test_first_tool_no_go(self):
        string = """ID,set1,set2
id1,,GO:0070279"""
        expected = (["id1"],
                    [[]],
                    [['GO:0070279']])
        self.do_test(string, expected)

    def test_no_header_first_tool_no_go(self):
        string = """id1,,GO:0070279"""
        expected = (["id1"],
                    [[]],
                    [['GO:0070279']])
        self.do_test(string, expected)


class TestPlotSimilarity(unittest.TestCase):
    '''Unit tests for plot_similarity'''

    def do_test(self, list_similarity_values, expected_exception=None):
        "Wrapper function for testing plot_similarity"
        if expected_exception:
            with self.assertRaises(expected_exception):
                plot_similarity(list_similarity_values)
        else:
            result = plot_similarity(list_similarity_values)
            self.assertTrue(isinstance(result, matplotlib.figure.Figure))

    def test_single_val(self):
        lst = [1]
        self.do_test(lst)

    def test_multi_val(self):
        lst = [3,5,9.]
        self.do_test(lst)

    def test_mixed_types(self):
        lst = [3,"wasd",5]
        self.do_test(lst, ValueError)


if __name__ == '__main__':
    unittest.main()
