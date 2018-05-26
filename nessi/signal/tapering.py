#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: tapering.py
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
        if i == 0:
            ftap[i] = 0.
        else:
            ftap[i] = float(i)/float(ntap1)
    for i in range(0, ntap2):
        if i == 0:
            ftap[n-i-1] = 0.
        else:
            ftap[n-i-1] = float(i)/float(ntap2)

    return ftap

def _sine(n, ntap1, ntap2):
    """
    Sine taper type.
    """
    # Initialize taper function
    ftap = np.zeros(n, dtype=np.float32)
    ftap[:] = 1

    # Create the taper function
    for i in range(0, ntap1):
        if i == 0:
            ftap[i] = 0.
        else:
            ftap[i] = np.sin(np.pi*float(i)/float(ntap1)/2.)
    for i in range(0, ntap2):
        if i == 0:
            ftap[n-i-1] = 0.
        else:
            ftap[n-i-1] = np.sin(np.pi*float(i)/float(ntap2)/2.)

    return ftap

def _cosine(n, ntap1, ntap2):
    """
    Cosine taper type.
    """
    # Initialize taper function
    ftap = np.zeros(n, dtype=np.float32)
    ftap[:] = 1

    # Create the taper function
    for i in range(0, ntap1):
        if i == 0:
            ftap[i] = 0.
        else:
            ftap[i] = 0.5*(1.0-np.cos(np.pi*float(i)/float(ntap1)))
    for i in range(0, ntap2):
        if i == 0:
            ftap[n-i-1] = 0.
        else:
            ftap[n-i-1] = 0.5*(1.0-np.cos(np.pi*float(i)/float(ntap2)))

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
    if type == 'linear':
        ftap = _linear(n, ntap1, ntap2)
    if type == 'sine':
        ftap = _sine(n, ntap1, ntap2)
    if type == 'cosine':
        ftap = _cosine(n, ntap1, ntap2)

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
