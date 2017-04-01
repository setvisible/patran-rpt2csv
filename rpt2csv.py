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

global_verbose = True

def main():
    parser = OptionParser(usage="usage: %prog [options] filename", version="1.0")
    parser.add_option("-o", "--output", dest="output_file_name",
                      help="Write result to FILE",
                      metavar="FILE")
    parser.add_option("-e", "--ends-with", dest="ends_with",
                      help="Look for the first line in the header that ends with STRING",
                      default=", Static Subcase", metavar="STRING")
    parser.add_option("-s", "--substring", dest="sub_string",
                      help="Populate the first column with string at RANGE. "
                      + "Must be 'a:b', where a and b are integers.",
                      default="-33:6", metavar="RANGE")
    parser.add_option("-q", "--quiet", dest="verbose",
                      help="Don't print status messages to stdout",
                      default=True, action="store_false")

    (options, args) = parser.parse_args()
    output_file_name = options.output_file_name
    ends_with = options.ends_with
    sub_string = options.sub_string
    _set_verbose(options.verbose)

    if len(args) != 1:
        parser.error("wrong number of arguments")

    input_file_name = args[0]

    # Increment the output filename to not overwrite
    if not output_file_name:
        incr = 0
        while True:
            ext = "_csv-friendly_" + str(incr) + ".rpt"
            output_file_name = os.path.basename(input_file_name) + ext
            if not os.path.exists(output_file_name): break
            incr = incr + 1

    if not ends_with:
        parser.error("No 'ends with' string. Please define the -e.")

    if not sub_string:
        parser.error("No substring to populate. Please define the -s.")

    try:
        start, length = map(int, sub_string.split(':'))
    except:
        parser.error("-s argument must be 'a:b', where a and b are integers.")

    if not os.path.exists(input_file_name):
        parser.error("File '%s' not found." % input_file_name)

    if os.path.exists(output_file_name):
        parser.error("File '%s' already exists. End of the script."\
                     % output_file_name)


    _process(input_file_name, output_file_name, ends_with, start, length)


def _set_verbose(verbose):
    global global_verbose
    global_verbose = verbose

def _is_verbose():
    global global_verbose
    return global_verbose

def _info(text):
    global global_verbose
    if global_verbose:
        print text

def _read_file(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()

def _write_file(lines, file_name):
    with open(file_name, 'w') as file:
        file.writelines(lines)


def _process(input_file_name, output_file_name, ends_with, start, length):

    _info("reading \"%s\"..." % input_file_name)
    text = _read_file(input_file_name)

    converted_text = _convert_text(text, ends_with, start, length)

    _info("writing \"%s\"..." % output_file_name)
    _write_file(converted_text, output_file_name)

    _info("End of the script.")


def _convert_text(text, ends_with, start, length):

    _info("copying substring from column %s (length %s) "\
          "in lines ending with '%s'..." % (start, length, ends_with) )

    is_content = False
    current_subcase = ""
    subcases_count = 0
    list_1 = [];

    for line in text:

        trimmed_line = line.strip()
        if trimmed_line.startswith("MSC.Patran"):
            is_content = False
            current_subcase = ""
            continue

        if trimmed_line.endswith(ends_with):
            _info("trimmed : %s" % trimmed_line)
            current_subcase = trimmed_line[start:start+length]
            _info("current_subcase : %s" % current_subcase)
            subcases_count = subcases_count + 1
            _info("found \"%s\"..." % current_subcase)
            continue

        if line.startswith("--Entity ID--"):
            is_content = True
            if len(list_1) == 0:
                separator = '*' * length        # repeat n times char '*'
                list_1.append("%s--%s" % (separator, line) )
            continue

        if is_content:
            list_1.append("%s  %s" % (current_subcase, line) )

    _info("Total found %s occurrences..." % subcases_count)
    return list_1



if __name__ == '__main__':
    main()
