import unittest

from src.generic_utils import parse_int, parse_sample_file


class ParseIntTests(unittest.TestCase):
    def test_parse_int_with_valid_integer1(self):
        self.assertAlmostEqual(1, parse_int('1'))

    def test_parse_int_with_valid_integer2(self):
        self.assertAlmostEqual(-2, parse_int('-2'))

    def test_parse_int_with_valid_integer3(self):
        self.assertAlmostEqual(0, parse_int('0'))

    def test_parse_int_with_valid_float1(self):
        self.assertIs(None, parse_int('3.0'))

    def test_parse_int_with_valid_float2(self):
        self.assertIs(None,  parse_int('-4.0'))

    def test_parse_int_with_valid_float3(self):
        self.assertIs(None,  parse_int('0.0'))

    def test_parse_int_with_invalid_number1(self):
        self.assertIs(None, parse_int('abcd'))

    def test_parse_int_with_invalid_number2(self):
        self.assertIs(None, parse_int(''))

    def test_parse_int_with_invalid_number3(self):
        self.assertIs(None, parse_int('1xyz'))


class ParseSamplesFileTests(unittest.TestCase):
    def test_parse_sample_file(self):
        parsed_samples = parse_sample_file('example_sample.txt')
        expected_samples = [1.0, 1.0, 2.0, 1.0, 3.0, 2.0]
        self.assertEqual(len(expected_samples), len(parsed_samples))
        for i in range(len(parsed_samples)):
            self.assertAlmostEqual(expected_samples[i], parsed_samples[i])


if __name__ == '__main__':
    unittest.main()
