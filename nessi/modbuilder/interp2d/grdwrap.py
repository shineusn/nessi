#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: grdwrap.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Functions for coarse grid to fine grid interpolation.

:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from numpy import loadtxt, zeros, float32, ascontiguousarray
from ctypes import CDLL, c_int, c_float
from numpy.ctypeslib import ndpointer, load_library


def voronoi(npts, xp, zp, val, n1, n2, dh):
    """
    voronoi
    Coarse inversion gird to fine modelling grid using
    Voronoi tesselation.
    """

    # GRD library
    path = os.path.abspath(__file__)
    dirpath = os.path.dirname(path)
    clibgrd = load_library('libgrd', dirpath)

    # nessi_grd_vrn
    clibgrd.nessi_grd_vrn.argtypes = [c_int,
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      c_int, c_int, c_float,
                                      ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS')]

    # initalize models array
    model = zeros((n1, n2), dtype=float32, order='C')

    # convert to C order
    xp = ascontiguousarray(xp, dtype=float32)
    zp = ascontiguousarray(zp, dtype=float32)
    val = ascontiguousarray(val, dtype=float32)

    # call nessi_grd_vrn
    clibgrd.nessi_grd_vrn(npts, xp, zp, val, n1, n2, dh, model)

    return model


def idweight(npts, xp, zp, val, pw, n1, n2, dh):
    """
    voronoi
    Coarse inversion gird to fine modelling grid using
    Voronoi tesselation.
    """

    # GRD library
    path = os.path.abspath(__file__)
    dirpath = os.path.dirname(path)
    clibgrd = load_library('libgrd', dirpath)

    # nessi_grd_vrn
    clibgrd.nessi_grd_idw.argtypes = [c_int,
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      c_int, c_int, c_float, c_int,
                                      ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS')]

    # initalize models array
    model = zeros((n1, n2), dtype=float32, order='C')

    # convert to C order
    xp = ascontiguousarray(xp, dtype=float32)
    zp = ascontiguousarray(zp, dtype=float32)
    val = ascontiguousarray(val, dtype=float32)

    # call nessi_grd_vrn
    clibgrd.nessi_grd_idw(npts, xp, zp, val, n1, n2, dh, pw, model)

    return model

def sibson(npts, xp, zp, val, n1, n2, dh):
    """
    voronoi
    Coarse inversion gird to fine modelling grid using
    Voronoi tesselation.
    """

    # GRD library
    path = os.path.abspath(__file__)
    dirpath = os.path.dirname(path)
    clibgrd = load_library('libgrd', dirpath)

    # nessi_grd_vrn
    clibgrd.nessi_grd_sib.argtypes = [c_int,
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      ndpointer(dtype=float32, ndim=1, flags='C_CONTIGUOUS'),
                                      c_int, c_int, c_float,
                                      ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS')]

    # initalize models array
    model = zeros((n1, n2), dtype=float32, order='C')

    # convert to C order
    xp = ascontiguousarray(xp, dtype=float32)
    zp = ascontiguousarray(zp, dtype=float32)
    val = ascontiguousarray(val, dtype=float32)

    # call nessi_grd_vrn
    clibgrd.nessi_grd_sib(npts, xp, zp, val, n1, n2, dh, model)

    return model
