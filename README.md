# Patran Report to CSV (rpt2csv)

## Description

A simple tool to convert Patran Report format (RPT) into an exportable table for Calc or Excel (CSV).

The tool works on Windows, Mac OS X and Unix.


## Usage

The command

    rpt2csv.py myfile.rpt

writes the converted table in `filename_csv-friendly_0.rpt` in the same directory as the input file.


Usage:

    rpt2csv.py [options] filename

Options:

      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o FILE, --output=FILE
                            Write result to FILE
      -e STRING, --ends-with=STRING
                            Look for the first line in the header that ends with
                            STRING
      -s RANGE, --substring=RANGE
                            Populate the first column with string at RANGE. Must
                            be 'a:b', where a and b are integers.
      -q, --quiet           Don't print status messages to stdout

