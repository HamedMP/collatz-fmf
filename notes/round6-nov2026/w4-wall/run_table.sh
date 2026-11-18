#!/bin/sh
PY=/home/matrix/home/projects/collatz/venv/bin/python
$PY n2_table.py 800 1 3 1 200,400,800
$PY n2_table.py 800 5 3 1 800
$PY n2_table.py 800 7 3 1 800
$PY n2_table.py 800 1 5 1 800
$PY n2_table.py 800 1 3 -1 800
$PY n2_table.py 1600 1 3 1 1600
$PY n2_table.py 3200 1 3 1 3200
