#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: windowing.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
.. module:: su_fmt
    :synopsis: Seismic Unix format support.
.. moduleauthor:: Damien Pageot (nessi.develop@protonmail.com)
"""

import numpy as np

def _linear(n, ntap1, ntap2):
    """
    Linear taper type.
    """
    # Initialize taper function
    ftap = np.zeros(n, dtype=np.float32)
    ftap[:] = 1

    # Create the taper function
    for i in range(0, ntap1):
        ftap[i] = float(i)/float(ntap1-1)
    for i in range(n-ntap2+1, n):
        ftap[i] = float(n-i-1)/float(ntap2-1)

    return ftap

def taper1d(dobs, ntap1, ntap2, min, type, axis=0):
    """
    Taper data.
    """

    dobstaper = np.zeros(np.shape(dobs), dtype=np.float32)

    # Get the number of dimensions of dobs
    if dobs.ndim == 1:
        n = 1
    if dobs.ndim == 2:
        if axis == 0:
            n = np.size(dobs, axis=0)
        else:
            n = np.size(dobs, axis=1)

    # Calculate the taper function
    ftap = _linear(n, ntap1, ntap2)

    # Apply the taper function
    if n == 1:
        dobstaper[:] = dobs[:]*ftap[:]
    else:
        if axis == 0:
            for i in range(0, np.size(dobs, axis=1)):
                dobstaper[:, i] = dobs[:, i]*ftap[:]
            #print(dobs[:, 0],'\n',ftap[:],'\n',dobs[:, 0]*ftap[:])
        if axis == 1:
            for i in range(0, np.size(dobs, axis=0)):
                dobstaper[i, :] = dobs[i, :]*ftap[:]
            #print(dobs[0, :],'\n',ftap[:],'\n',dobs[0, :]*ftap[:])

    return dobstaper
