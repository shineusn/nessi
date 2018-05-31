#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: test_gpdcwrap.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Test suite for the Geopsy-gpdc interface (nessi.modeling.interfaces)

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
from nessi.modeling.interfaces import dispersion_curve_init
from nessi.modeling.interfaces import dispersion_curve_rayleigh
from nessi.modeling.interfaces import dispersion_curve_love

def test_dispersion_curve_rayleigh():
    """
    dispersion_curve_rayleigh test following the example
    from the geopsy wiki.
    """

    # Attempted output
    output = np.array([0.00514753, 0.00516327, 0.00517777, 0.00519118,
                       0.00520354, 0.00521485, 0.00522513, 0.00523439,
                       0.00524268, 0.00525007, 0.00525662, 0.0052624,
                       0.00526749, 0.00527197, 0.00527589, 0.00527933,
                       0.00528233, 0.00528496, 0.00528725, 0.00528925,
                       0.005291,   0.00529253, 0.00529386, 0.00529502,
                       0.00529603, 0.00529692, 0.00529769, 0.00529836,
                       0.00529895, 0.00529947, 0.00529991, 0.00530031,
                       0.00530065, 0.00530095, 0.00530121, 0.00530144,
                       0.00530164, 0.00530181, 0.00530196, 0.0053021,
                       0.00530221, 0.00530232, 0.0053024,  0.00530248,
                       0.00530255, 0.00530261, 0.00530266, 0.00530271,
                       0.00530275, 0.00530278, 0.00530281], dtype=np.float64)

    # Define the model
    nLayers = 3
    h = np.zeros(nLayers, dtype=np.float64)
    vp = np.zeros(nLayers, dtype=np.float64)
    vs = np.zeros(nLayers, dtype=np.float64)
    rho = np.zeros(nLayers, dtype=np.float64)

    h[0] = 7.5
    h[1] = 25.0
    vp[0] = 500.0
    vp[1] = 1350.0
    vp[2] = 2000.0
    vs[0] = 200.0
    vs[1] = 210.0
    vs[2] = 1000.0
    rho[0] = 1800.0
    rho[1] = 1900.0
    rho[2] = 2500.0

    # Frequency sample
    nSamples = 51
    omega = np.linspace(10., 50., 51)
    omega *= 2.*np.pi

    # Number of modes and output option (0=phase, 1=group slowness)
    nModes = 1
    group = 0

    # Create the output array
    slowness = np.zeros((nSamples*nModes), dtype=np.float64)

    # Calculate theoretical Rayleigh dispersion curve
    dispersion_curve_rayleigh(nLayers, h, vp, vs, rho, nSamples, omega, nModes, slowness, group)

    # Testing the output slowness curve
    np.testing.assert_allclose(slowness, output, atol=1.e-7)

def test_dispersion_curve_love():
    """
    dispersion_curve_love test following the example
    from the geopsy wiki.
    """

    # Attempted output
    output = np.array([0.00481211, 0.00482421, 0.0048346 , 0.00484373, 0.00485189,
                       0.00485929, 0.00486608, 0.00487236, 0.00487821, 0.00488369,
                       0.00488883, 0.00489366, 0.00489822, 0.00490252, 0.00490657,
                       0.00491041, 0.00491404, 0.00491747, 0.00492071, 0.00492378,
                       0.0049267 , 0.00492945, 0.00493207, 0.00493455, 0.00493691,
                       0.00493915, 0.00494127, 0.00494329, 0.00494522, 0.00494705,
                       0.00494879, 0.00495046, 0.00495204, 0.00495356, 0.004955  ,
                       0.00495638, 0.0049577 , 0.00495896, 0.00496017, 0.00496133,
                       0.00496244, 0.0049635 , 0.00496452, 0.00496549, 0.00496643,
                       0.00496733, 0.0049682 , 0.00496903, 0.00496983, 0.0049706 ,
                       0.00497134], dtype=np.float64)

    # Define the model
    nLayers = 3
    h = np.zeros(nLayers, dtype=np.float64)
    vp = np.zeros(nLayers, dtype=np.float64)
    vs = np.zeros(nLayers, dtype=np.float64)
    rho = np.zeros(nLayers, dtype=np.float64)

    h[0] = 7.5
    h[1] = 25.0
    vp[0] = 500.0
    vp[1] = 1350.0
    vp[2] = 2000.0
    vs[0] = 200.0
    vs[1] = 210.0
    vs[2] = 1000.0
    rho[0] = 1800.0
    rho[1] = 1900.0
    rho[2] = 2500.0

    # Frequency sample
    nSamples = 51
    omega = np.linspace(10., 50., 51)
    omega *= 2.*np.pi

    # Number of modes and output option (0=phase, 1=group slowness)
    nModes = 1
    group = 0

    # Create the output array
    slowness = np.zeros((nSamples*nModes), dtype=np.float64)

    # Calculate theoretical Rayleigh dispersion curve
    dispersion_curve_love(nLayers, h, vp, vs, rho, nSamples, omega, nModes, slowness, group)

    # Testing the output slowness curve
    np.testing.assert_allclose(slowness, output, atol=1.e-7)

if __name__ == "__main__" :
    # Initialize application instance here because one instance at a time only
    dispersion_curve_init(0)

    # Run test suite
    np.testing.run_module_suite()
