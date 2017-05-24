echo off
set mypath=%~dp0
rem echo %mypath:~0,-1%
set arg1=%1
python %mypath:~0,-1%\rpt2csv.py %arg1%
pause
