# -*- coding: utf-8 -*-
"""
*******************************************************************************
RPT2CSV (Patran Report to CSV Format) (Patran's Hack)
*******************************************************************************

Convert the Patran RPT report format
into an exportable table for Calc or Excel.

1) Search lines ending with ", Static Subcase" and take the
   substring "-33:6" containing the loadcase name.

2) Prepend all the rows with a new column containing this substring.

3) Erase the titles in order to have continuous tables.

"""
import os.path
from optparse import OptionParser


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main():
    parser = OptionParser(usage="usage: %prog [options] filename", version="1.0")
    parser.add_option("-o", "--output", dest="outputfilename",
                      help="Write result to FILE",
                      metavar="FILE")
    parser.add_option("-e", "--ends-with", dest="endswith",
                      help="Look for the first line in the header that ends with STRING",
                      default=", Static Subcase", metavar="STRING")
    parser.add_option("-s", "--substring", dest="substring",
                      help="Populate the first column with string at RANGE. "
                      + "Must be 'a:b', where a and b are integers.",
                      default="-33:6", metavar="RANGE")
    parser.add_option("-q", "--quiet", dest="verbose",
                      help="Don't print status messages to stdout",
                      default=True, action="store_false")
    
    (options, args) = parser.parse_args()
    outputfilename = options.outputfilename
    endswith = options.endswith
    substring = options.substring
    verbose = options.verbose
        
    if len(args) != 1:
        parser.error("wrong number of arguments")
        
    inputfilename = args[0]
    
    # Increment the output filename to not overwrite
    if not outputfilename:
        incr = 0
        while True:
            ext = "_csv-friendly_" + str(incr) + ".rpt"
            outputfilename = os.path.basename(inputfilename) + ext
            if not os.path.isfile(outputfilename): break
            incr = incr + 1
            
    if not endswith:
        parser.error("No 'ends with' string. Please define the -e.")
    
    if not substring:
        parser.error("No substring to populate. Please define the -s.")
    
    rangeList = substring.split(':', 1 )
    if len(rangeList) != 2 \
    or not RepresentsInt( rangeList[0] ) \
    or not RepresentsInt( rangeList[1] ) :
        parser.error("-s argument must be 'a:b', where a and b are integers.")
    
    start = int(rangeList[0])
    length = int(rangeList[1])
    
    if not os.path.isfile(inputfilename):
        parser.error("File '%s' not found." % inputfilename)
        
    if os.path.isfile(outputfilename):
        parser.error("File '%s' already exists. End of the script."\
                     % outputfilename)
    
    
    c = Convertor()
    c.setVerbose(verbose)
    c.process(inputfilename, outputfilename, endswith, start, length)


class Convertor:
    
    verbose = True
    
    def setVerbose(self, verbose):
        self.verbose = verbose
        
    def isVerbose(self):
        return self.verbose
        
    def info(self, text):
        if self.verbose:
            print text
    
    def readFile(self, filename):
        file = open(filename,"r")
        text = file.readlines()
        file.close()
        return text
        
    def writeFile(self, result, filename):
        file = open(filename,"w")
        for item in result:
            file.write("%s" % item)
        file.close()
        
        
    def process(self, inputfilename, outputfilename, endswith, start, length):
        
        self.info("reading \"%s\"..." % inputfilename)
        text = self.readFile(inputfilename)
        
        result = self.convertText(text, endswith, start, length)
        
        self.info("writing \"%s\"..." % outputfilename)
        self.writeFile(result, outputfilename)
        
        self.info("End of the script.")
        
    
    def convertText(self, text, endswith, start, length):
            
        self.info("copying substring from column %s (length %s) "\
                  "in lines ending with '%s'..." % (start, length, endswith) )
        
        isContent = False
        currentcase = ""
        countcase = 0
        list1 = [];
        
        for line in text:
        
            trimmed = line.strip()
            if trimmed.startswith("MSC.Patran"):
                isContent = False
                currentcase = ""
                continue
            
            if trimmed.endswith(endswith):
                self.info("trimmed : %s" % trimmed)
                currentcase = trimmed[start:start+length]
                self.info("currentcase : %s" % currentcase)
                countcase = countcase + 1
                self.info("found \"%s\"..." % currentcase)
                continue
                
            if line.startswith("--Entity ID--"):
                isContent = True
                if len(list1) == 0:
                    separator = '*' * length        # repeat n times char '*'
                    list1.append("%s--%s" % (separator, line) )
                continue
                
            if isContent:
                list1.append("%s  %s" % (currentcase, line) )
        
        self.info("Total found %s occurrences..." % countcase)
        return list1
        
        
        
if __name__ == '__main__':
    main()
