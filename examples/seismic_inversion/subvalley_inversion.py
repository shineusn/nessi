#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: subvalley_inversion.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Inversion of Rayleigh dispersion diagrams using PSO.
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
import seismod


# ------------------------------------------------------------------
# >> Seismic modeling parameters
# ------------------------------------------------------------------

# >> Run parameters
runpar = {
    'name': 'subvalley',
    # Time marching
    'tmax': 1.0, 'dt': 0.0001,
    # Snapshots
    'snap': 0, 'dtsnap': 0.001}

# >> Model grid parameters
modpar = {
    # Grid dimensions
    'n1': 51, 'n2': 301, 'dh': 0.5,
    # Boundary conditions
    'ifsurf': 1, 'npml': 20, 'apml': 2000., 'ppml': 8}

# >> Acquisition parameters
acqpar = {
    # Source parameters
    'sx': 10., 'sz': 0.5, 'f0': 15., 't0': 0.1, 'spread': -1, 'type': 2,
    # Receiver file name and data sampling
    'facqui': 'input/acquisition.dat ', 'dts': 0.0001}


# ------------------------------------------------------------------
# >> Seismic velocity and density models
# ------------------------------------------------------------------

n1g = modpar['n1']
n2g = modpar['n2']
modvp = np.fromfile('input/fvp.bin', dtype=np.float32)
modvp = (modvp.reshape(n2g, n1g)).swapaxes(1, 0)
modvs = np.fromfile('input/fvs.bin', dtype=np.float32)
modvs = (modvs.reshape(n2g, n1g)).swapaxes(1, 0)
modro = np.fromfile('input/fro.bin', dtype=np.float32)
modro = (modro.reshape(n2g, n1g)).swapaxes(1, 0)


# ------------------------------------------------------------------
# >> Seismic modeling
# ------------------------------------------------------------------

recx, recz, recp = seismod.modeling(runpar, modpar, acqpar,
                                    modvp, modvs, modro)
