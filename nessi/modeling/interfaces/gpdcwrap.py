import numpy as np
from ctypes import CDLL, c_int, c_float, byref, POINTER, c_double
from numpy.ctypeslib import ndpointer, load_library
from nessi import QGPCOREWAVE_PATH

import matplotlib.pyplot as plt

libCoreWave = load_library('libQGpCoreWave', QGPCOREWAVE_PATH)

def dispersion_curve_init(verbose):
    libCoreWave.dispersion_curve_init_.argtypes = [POINTER(c_int)]
    libCoreWave.dispersion_curve_init_(byref(c_int(verbose)))
    return

def dispersion_curve_rayleigh(nLayers, h, vp, vs, rho, nSamples, omega, nModes, slowness, group):
    libCoreWave.dispersion_curve_rayleigh_.argtypes = [ POINTER(c_int),
                                                        ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                        ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                        ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                        ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                        POINTER(c_int),
                                                        ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                        POINTER(c_int),
                                                        ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                        POINTER(c_int)]
    
    libCoreWave.dispersion_curve_rayleigh_(byref(c_int(nLayers)),
                                           h,
                                           vp,
                                           vs,
                                           rho,
                                           byref(c_int(nSamples)),
                                           omega,
                                           byref(c_int(nModes)),
                                           slowness,
                                           byref(c_int(group)))
    return

def dispersion_curve_love(nLayers, h, vp, vs, rho, nSamples, omega, nModes, slowness, group):
    libCoreWave.dispersion_curve_love_.argtypes = [ POINTER(c_int),
                                                    ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                    ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                    ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                    ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                    POINTER(c_int),
                                                    ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                    POINTER(c_int),
                                                    ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                                                    POINTER(c_int)]
    
    libCoreWave.dispersion_curve_love_(byref(c_int(nLayers)),
                                       h,
                                       vp,
                                       vs,
                                       rho,
                                       byref(c_int(nSamples)),
                                       omega,
                                       byref(c_int(nModes)),
                                       slowness,
                                       byref(c_int(group)))
    return
