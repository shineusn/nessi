#!/bin/bash

cythonize -a -i grdinterp.pyx
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/home/pageotd/miniconda3/envs/nessi3.6/include/python3.6m/ -o grdinterp.so grdinterp.c
