"""
Unit tests for megago.

Usage: python -m unittest -v megago_test
"""

import unittest
from io import StringIO
# pylint: disable=no-name-in-module
from megago import read_input


class TestFastaStats(unittest.TestCase):
    '''Unit tests for FastaStats'''

    def do_test(self, input_str, expected):
        "Wrapper function for testing FastaStats"
        result = read_input(StringIO(input_str))
        self.assertEqual(expected, result)

    def test_zero_byte_input(self):
        "Test input containing zero bytes"
        expected = [], []
        self.do_test('', expected)

    def test_valid_go_terms(self):
        string = """GO:0005488,GO:0048037;GO:0036094
GO:0098581,GO:0032490;GO:0098543
GO:0050789,GO:0030155;GO:0031341"""
        expected = ([['GO:0005488'], ['GO:0098581'], ['GO:0050789']],
                    [['GO:0048037', 'GO:0036094'],
                     ['GO:0032490', 'GO:0098543'],
                     ['GO:0030155', 'GO:0031341']])
        self.do_test(string, expected)

    def test_second_tool_no_go_terms(self):
        string = """GO:0098581,
GO:0050789,GO:0030155;GO:0031341"""
        expected = ([['GO:0098581'], ['GO:0050789']],
                    [[],
                     ['GO:0030155', 'GO:0031341']])
        self.do_test(string, expected)

    def test_first_tool_no_go(self):
        string = """set1,set2
,GO:0070279"""
        expected = ([[]],
                    [['GO:0070279']])
        self.do_test(string, expected)

    def test_no_header_first_tool_no_go(self):
        string = """,GO:0070279"""
        expected = ([[]],
                    [['GO:0070279']])
        self.do_test(string, expected)


if __name__ == '__main__':
    unittest.main()
