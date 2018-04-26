from numpy import loadtxt, zeros, float32, ascontiguousarray, isfortran
from ctypes import CDLL, c_int, c_float
from numpy.ctypeslib import ndpointer, load_library

def modext(n1, n2, npml, v):

    # load libswm
    clibswm = load_library('libswm',
                               '/home/pageotd/Work/nessi/nessi/swm/')

    # nessi_swm_modext argtypes
    clibswm.nessi_swm_modext.argtypes = [c_int, c_int, c_int,
                                         ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS'),
                                         ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS')]

    # allocate extended model array
    ve = zeros((n1+2*npml, n2+2*npml), dtype=float32, order='C')

    # test original model order
    if(isfortran(v)):
        v = ascontiguousarray(v, dtype=float32)
        
    # call nessi_swm_modext
    clibswm.nessi_swm_modext(n1, n2, npml, v, ve)

    return ve
