#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: pso_peaks.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Seismic modeling class.
:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

import numpy as np

from . import modext
from . import modbuo
from . import modlame
from . import acqpos
from . import pmlmod
from . import ricker
from . import srcspread
from . import evolution


class Seismod():
    """
    Seismod class aims to facilitate the use of the 2D P-Sv seismic
    modeling engine.
    """

    def __inti__(self):
        """
        Initialize Seismod parameters
        """

        # >> Run parameters
        self.tmax = 1.0
        self.dt = 0.0001

        # >> Grid
        self.modelgrid = ModelGrid()

        # >> Boundaries parameters
        self.isurf = 1 # Free surface
        self.pml = (20, 6000., 32) # PML parameters (npml, apml, ppml)

        # >> Acquisition parameters
        self.receivers = np.zeros((1, 2), dtype=np.float32)
        self.dts = 0.0001

        # >> Source parameters
        self.srcpos = (10.0, 0.5) # Source position in (x, z)
        self.srcpar = (15.0, 0.1) # Source parameters (f0, t0)
        self.sigma = -1.
        self.srctype = 2

        # >> Snapshots
        self.isnap = 0
        self.dtsnap = 0.001

class ModelGrid(object):
    """
    Class to handle modeling grid parameters and functions
    """
    def __init__(self):
        """
        Initialize grid parameters
        """
        self.n1 = 0
        self.n2 = 0
        self.dh = 0.
