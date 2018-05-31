#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: gpdcwrap.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Functions to use the Geopsy-gpdc engine.

:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from ctypes import CDLL, c_int, c_float, byref, POINTER, c_double
from numpy.ctypeslib import ndpointer, load_library
from nessi import QGPCOREWAVE_PATH

import matplotlib.pyplot as plt

libCoreWave = load_library('libQGpCoreWave', QGPCOREWAVE_PATH)

def dispersion_curve_init(verbose):
    """
    Initialize the dispersion curve calculation.

    :param verbose: integer, 0 minimal ouput, 1 verbose output
    """
    libCoreWave.dispersion_curve_init_.argtypes = [POINTER(c_int)]
    libCoreWave.dispersion_curve_init_(byref(c_int(verbose)))
    return

def dispersion_curve_rayleigh(nLayers, h, vp, vs, rho, nSamples, omega, nModes, slowness, group):
    """
    Calculate the Rayleigh theoretical dispersion curve.

    :param nLayers: integer, number of layers
    :param h: double, thickness of layers (m)
    :param vp: double, P-wave velocity in each layer (m/s)
    :param vs: double, S-wave velocity in each layer (m/s)
    :param rho: double, density in each layer (kg/m3)
    :param nSamples: integer, number of frequency samples
    :param omega: double, angular frequencies (rad/s)
    :param nModes: integer, number of modes including fundamental
    :param slowness: double, output of slowness values
    :param group: integer, 0 for phase, 1 for group
    """
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
    """
    Calculate the Love theoretical dispersion curve.

    :param nLayers: integer, number of layers
    :param h: double, thickness of layers (m)
    :param vp: double, P-wave velocity in each layer (m/s)
    :param vs: double, S-wave velocity in each layer (m/s)
    :param rho: double, density in each layer (kg/m3)
    :param nSamples: integer, number of frequency samples
    :param omega: double, angular frequencies (rad/s)
    :param nModes: integer, number of modes including fundamental
    :param slowness: double, output of slowness values
    :param group: integer, 0 for phase, 1 for group
    """
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
