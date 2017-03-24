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

class TestConvertor(unittest.TestCase):

    def runTestFile(self, inputFileName, expectedFileName):
        """
        Unit test
        """
        
        self.assertTrue(inputFileName, "Error: null or empty string")
        self.assertTrue(expectedFileName, "Error: null or empty string")
        
        inputFile = open(inputFileName,"r")
        inputText = inputFile.readlines()
        inputFile.close()
        
        expectedFile = open(expectedFileName,"r")
        expectedText = expectedFile.readlines()
        expectedFile.close()
        
        self.assertTrue(inputText, "Error: null or empty string")
        self.assertTrue(expectedText, "Error: null or empty string")
        
        target = rpt2csv.Convertor()
        target.setVerbose(False)
        actualText = target.convertText(inputText, ", Static Subcase", -33, 6)
        
        # Debugging
        logging.debug(inputText)
        logging.debug(expectedText)
        logging.debug(actualText)
        
        self.assertItemsEqual(actualText, expectedText)
        
        
    def test_simple_files(self):
        self.runTestFile("test_simple/test_001_input.rpt", "test_simple/test_001_expected.rpt")
        self.runTestFile("test_simple/test_002_input.rpt", "test_simple/test_002_expected.rpt")
        self.runTestFile("test_simple/test_003_input.rpt", "test_simple/test_003_expected.rpt")
        self.runTestFile("test_simple/test_004_input.rpt", "test_simple/test_004_expected.rpt")
        self.runTestFile("test_simple/test_005_input.rpt", "test_simple/test_005_expected.rpt")
        
        
    def test_empty_file(self):
        target = rpt2csv.Convertor()
        target.setVerbose(False)
        text = target.convertText("", "", 0, 0)
        self.assertFalse(text, "Error: not empty")
        
        
    def test_invalid_file(self):
        target = rpt2csv.Convertor()
        target.setVerbose(False)
        text = target.convertText("yoyo", "", 0, 0)
        self.assertFalse(text, "Error: not empty")
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConvertor)
    unittest.TextTestRunner(verbosity=2).run(suite)
