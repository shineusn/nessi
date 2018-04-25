from numpy import loadtxt, zeros, float32
from ctypes import CDLL, c_int, c_float
from numpy.ctypeslib import ndpointer, load_library

def dispfv(nv, nw, n1c, ns, nr, iwmin, v, w, dist, dobsc):
    
    # load libdsp
    clibdsp = load_library('libdsp', '/home/Work/pageotd/nessi/nessi/dsp/')
    
    # nessi_pso_init
    clibdsp.nessi_dsp_masw.argtypes = [c_int, c_int, c_int, c_int,
                                       c_int, c_int, 
                                       ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                       ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                       ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS'),
                                       ndpointer(dtype=complex64, ndim=2, flags='C_CONTIGUOUS'),
                                       ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS')]

    # allocate dispersion array
    disp = zeros((nv, nw), dtype=float32, order='C')

    # call nessi_dsp_masw function
    clibdsp.nessi_dsp_masw(nv, nw, n1c, ns, nr, iwmin, v, w, dist, dobsc, disp)

    return disp

def smooth(nv, nw, dv, dw, v, w, sgv, sgw, disp):
    
    # load libdsp
    clibdsp = load_library('libdsp', '/home/Work/pageotd/nessi/nessi/dsp/')
    
    # nessi_pso_init
    clibdsp.nessi_dsp_gsmooth.argtypes = [c_int, c_int, c_float, c_float,
                                          ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                          ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                          c_float, c_float,
                                          ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS'),
                                          ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS')]

    # allocate smooth dispersion array
    dispg = zeros((nv, nw), dtype=float32, order='C')

    # call nessi_dsp_masw function
    clibdsp.nessi_dsp_gsmooth(nv, nw, dv, dw, v, w, sgv, sgw, disp, dispg)

    return dispg
