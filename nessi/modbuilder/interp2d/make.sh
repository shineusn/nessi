#!/bin/bash

cythonize -a -i grdinterp.pyx
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing $(python3-config --includes) -o grdinterp.so grdinterp.c
