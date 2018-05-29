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
Data windowing functions.

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

def time_window(dobs, tmin=0.0, tmax=0.0, dt=0.01, delrt=0, axis=0):
    """
    Window traces in time.

    :param dobs: input data to window
    :param tmin: minimum time to pass (=0.0)
    :param tmax: maximum time to pass (=0.0)
    :param dt: time sampling (=0.01)
    :param delrt: delay recording time (=0.0)
    """

    # Get the number of traces
    if dobs.ndim == 1:
        ntrac = 1
    if dobs.ndim == 2:
        if axis == 0:
            ntrac = np.size(dobs, axis=1)
        else:
            ntrac = np.size(dobs, axis=0)

    # Calculate indices
    itmin = int((tmin-delrt)/dt)
    itmax = int((tmax-delrt)/dt)

    # Windowing
    if axis == 0:
        dobswind = dobs[itmin:itmax+1, :]
    if axis == 1:
        dobswind = dobs[:, itmin:itmax+1]

    return dobswind

def space_window(dobs, imin=0.0, imax=0.0, axis=0):
    """
    Window traces in space.

    :param dobs: input data to window
    :param imin: minimum value of trace to pass (=0)
    :param tmax: maximum value of trace to pass (=0)
    """
    # Windowing
    if axis == 0:
        dobswind = dobs[imin:imax+1, :]
    if axis == 1:
        dobswind = dobs[:, imin:imax+1]

    return dobswind
