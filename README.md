# Patran Report to CSV (rpt2csv)

## Description

A simple tool to convert Patran Report file into [CSV](https://en.wikipedia.org/wiki/Comma-separated_values "Comma-Separated Values (CSV)").

It is written in [Python](https://www.python.org/ "www.python.org") language.


## Features

The tool reads a Patran Report file (`*.rpt`) and converts it into
Comma-Separated Values (`*.csv`) readable by
[Calc](https://en.wikipedia.org/wiki/LibreOffice_Calc "LibreOffice Calc") or
[Excel](https://en.wikipedia.org/wiki/Microsoft_Excel "Microsoft Excel").


Basically, the command

    python .\rpt2csv.py my_report.rpt -o output.rpt -s -31:15


converts this:
        
                          MSC.Patran - Analysis Code: MSC.Nastran 
     
                      Load Case: SC15:MY_LOAD_CASE_01, Static Subcase 
     
                  Result Bushing Forces, Translational - Layer (NON-LAYERED) 
     
                                     Entity: Element Vector
    
    
    --Entity ID---Loadcase ID---X Component---Y Component---Z Component----CID---
         38352           3        533.480896   2461.196533   1804.358887       0
         38362           3       -130.094818   2401.134277     56.332920       0
         38382           3       -380.708374   2515.291748  -1849.518799       0
         38392           3       -183.099304   2705.627930  -1607.576050       0
         38402           3       -128.897537   2341.458496    266.653656       0
         38422           3        283.474365   2327.804688   1429.604126       0
                          MSC.Patran - Analysis Code: MSC.Nastran 
    
                      Load Case: SC7:MY_LOAD_CASE_02, Static Subcase 
    
                  Result Bushing Forces, Translational - Layer (NON-LAYERED) 
    
                                     Entity: Element Vector
    
    
    --Entity ID---Loadcase ID---X Component---Y Component---Z Component----CID---
         38352           4       -617.528870  -2996.874023  -1786.385864       0
         38362           4        148.421478  -2893.618652    -70.907944       0
         38382           4        413.402344  -3031.503174   1797.993530       0
         38392           4        262.724976  -3248.933350   1649.425659       0
         38402           4        152.307739  -2830.450928   -262.058075       0
         38422           4       -352.277924  -2840.288574  -1448.844238       0
    
    ...


into this:

    ***************--Entity ID---Loadcase ID---X Component---Y Component---Z Component----CID---
    MY_LOAD_CASE_01     38352           3        533.480896   2461.196533   1804.358887       0
    MY_LOAD_CASE_01     38362           3       -130.094818   2401.134277     56.332920       0
    MY_LOAD_CASE_01     38382           3       -380.708374   2515.291748  -1849.518799       0
    MY_LOAD_CASE_01     38392           3       -183.099304   2705.627930  -1607.576050       0
    MY_LOAD_CASE_01     38402           3       -128.897537   2341.458496    266.653656       0
    MY_LOAD_CASE_01     38422           3        283.474365   2327.804688   1429.604126       0
    MY_LOAD_CASE_02     38352           4       -617.528870  -2996.874023  -1786.385864       0
    MY_LOAD_CASE_02     38362           4        148.421478  -2893.618652    -70.907944       0
    MY_LOAD_CASE_02     38382           4        413.402344  -3031.503174   1797.993530       0
    MY_LOAD_CASE_02     38392           4        262.724976  -3248.933350   1649.425659       0
    MY_LOAD_CASE_02     38402           4        152.307739  -2830.450928   -262.058075       0
    MY_LOAD_CASE_02     38422           4       -352.277924  -2840.288574  -1448.844238       0
    ...



__Remarks:__

The substring `-s` defines the range "-31:15". That is, the tool looks for lines ending with ", Static Subcase" (see option `-e`), and copies the substring that begins at the **31th** character from the *end* of the line (*minus* 31), and that stops **15** characters after. It corresponds here to the loadcase names: "MY\_LOAD\_CASE\_01", "MY\_LOAD\_CASE\_02"...


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

