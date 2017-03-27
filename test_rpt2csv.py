# -*- coding: utf-8 -*-
"""
*******************************************************************************
Unit Test RPT2CSV (Patran Report to CSV Format) (Patran's Hack)
*******************************************************************************
"""
import rpt2csv
import unittest
import logging

### Uncomment the following lines for debugging:
#import sys
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
###

class TestRPT2CSV(unittest.TestCase):

    def _run_test_file(self, input_file_name, expected_file_name):
        """
        Unit test
        """

        self.assertTrue(input_file_name, "Error: null or empty string")
        self.assertTrue(expected_file_name, "Error: null or empty string")

        with open(input_file_name, 'r') as file:
            input_text = file.readlines()

        with open(expected_file_name, 'r') as file:
            expected_text = file.readlines()

        self.assertTrue(input_text, "Error: null or empty string")
        self.assertTrue(expected_text, "Error: null or empty string")

        rpt2csv._set_verbose(False)
        actual_text = rpt2csv._convert_text(input_text, ", Static Subcase", -33, 6)

        # Debugging
        logging.debug(input_text)
        logging.debug(expected_text)
        logging.debug(actual_text)

        self.assertItemsEqual(actual_text, expected_text)


    def test_simple_files(self):
        self._run_test_file("test_simple/test_001_input.rpt", "test_simple/test_001_expected.rpt")
        self._run_test_file("test_simple/test_002_input.rpt", "test_simple/test_002_expected.rpt")
        self._run_test_file("test_simple/test_003_input.rpt", "test_simple/test_003_expected.rpt")
        self._run_test_file("test_simple/test_004_input.rpt", "test_simple/test_004_expected.rpt")
        self._run_test_file("test_simple/test_005_input.rpt", "test_simple/test_005_expected.rpt")


    def test_empty_file(self):
        rpt2csv._set_verbose(False)
        text = rpt2csv._convert_text("", "", 0, 0)
        self.assertFalse(text, "Error: not empty")


    def test_invalid_file(self):
        rpt2csv._set_verbose(False)
        text = rpt2csv._convert_text("yoyo", "", 0, 0)
        self.assertFalse(text, "Error: not empty")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRPT2CSV)
    unittest.TextTestRunner(verbosity=2).run(suite)
