#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: seismic_modeling.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Seismic modeling example.
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
import matplotlib.pyplot as plt

from nessi.swm import SeisMod

from nessi.io import SUdata


# ------------------------------------------------------------
# >> Input parameters
# ------------------------------------------------------------

# >> Run parameters
jobname = 'test'
tmax = 1.0
dt = 0.0001

# >> Grid dimensions and node spacing
n1 = 51
n2 = 301
dh = 0.5

# >> Boundaries parameters
isurf = 1 # Free surface
npml = 20  # width in points of the PML bands
apml = 600.
ppml = 8

# >> Acquisition parameters
nrec = 48
drec = 2.0
xrec0 = 28.
zrec0 = dh
dts = 0.0001

# >> Source parameters
xs = 10.0; zs = 0.5 # source position
f0 = 15.0; t0 = 0.1 # peak frequency and t0
sigma = -1.
srctype = 2

# >> Snapshots
isnap = 0
dtsnap = 0.001


# ------------------------------------------------------------
# >> Calculate complementary parameters
# ------------------------------------------------------------
nt = int(tmax/dt)+1
nts = int(tmax/dts+1)
ntsnap = int(tmax/dtsnap)+1


# ------------------------------------------------------------
# >> Initialize SeisMod
# ------------------------------------------------------------

SM_run = SeisMod()


# ------------------------------------------------------------
# >> Generate input homogeneous models
# ------------------------------------------------------------

vp = np.zeros((n1, n2), dtype=np.float32)
vs = np.zeros((n1, n2), dtype=np.float32)
ro = np.zeros((n1, n2), dtype=np.float32)

vp[:, :] = 600.  # m/s
vs[:, :] = 200.  # m/s
ro[:, :] = 1500. # kg/m3

# Create extend models
SM_run.mod2phy(vp, vs, ro)

# Create PML boundary conditions
SM_run.modpml()


