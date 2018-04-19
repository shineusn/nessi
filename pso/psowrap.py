import ctypes as C
import numpy as np
from numpy.ctypeslib import ndpointer
import os

# >> Loading PSO shared library
clibpso = C.cdll.LoadLibrary(os.path.abspath("libpso.so"))

clibpso.nessi_pso_init.argtypes = [C.c_int, C.c_int, C.c_int,
                                   ndpointer(dtype=np.float32, ndim=3, flags='C_CONTIGUOUS'),
                                   ndpointer(dtype=np.float32, ndim=3, flags='C_CONTIGUOUS')]
