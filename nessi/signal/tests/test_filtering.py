#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: test_filtering.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Test suite for the filtering functions (nessi.signal.windowing)

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
from nessi.signal.filtering import sin2filter

def test_sin2filter_one_trac():
    """
    signal.filtering.sin2filter testing for one trace signal.
    """

    # Create initial data trace (Dirac)
    ns = 128   # number of time sample
    dt = 0.01 # time sampling
    dobs = np.zeros((ns), dtype=np.float32)
    dobs[63] = 1.0

    # Filter parameters
    freq = np.zeros(4, dtype=np.float32)
    amps = np.zeros(4, dtype=np.float32)
    freq[0] = 5.0
    freq[1] = 10.0
    freq[2] = 20.0
    freq[3] = 25.0
    amps[0] = 0.0
    amps[1] = 1.0
    amps[2] = 1.0
    amps[3] = 0.0

    # Filtering
    dobsf = sin2filter(dobs, freq, amps, dt)

    # Attempted output
    output = np.array(
            [0.00309653, 0.0012342, -0.00126124, -0.00360717, -0.00497581, -0.0047482,
            -0.00276421,  0.00053042,  0.00413397,  0.00677075,  0.00734182,  0.00538664,
            0.00135757, -0.00344372, -0.00729189, -0.00869041, -0.00699729, -0.00275275,
            0.00245907,  0.00659377,  0.00795973,  0.00593078,  0.00125195, -0.00421012,
            -0.00819097, -0.00894244, -0.0059648,  -0.00025205,  0.00605926,  0.01050454,
            0.01124905,  0.0078125,   0.00127966, -0.00607993, -0.01163275, -0.01333105,
            -0.0104439,  -0.0038142,   0.00443506,  0.01163002,  0.01545567,  0.01474424,
            0.00989041,  0.00276124, -0.00388159, -0.00728908, -0.00570489,  0.00087791,
            0.01044492,  0.01932639,  0.02318409,  0.01840399,  0.00350862, -0.0198769,
            -0.04690921, -0.07045032, -0.0828972,  -0.07845238, -0.0551515,  -0.01595536,
            0.03155101,  0.07688869,  0.10940884,  0.12121829,  0.10940884,  0.07688869,
            0.03155101, -0.01595536, -0.0551515,  -0.07845238, -0.0828972,  -0.07045032,
            -0.04690921, -0.0198769,   0.00350862,  0.01840399,  0.02318409,  0.01932639,
            0.01044492,  0.00087791, -0.00570489, -0.00728907, -0.00388159,  0.00276124,
            0.00989041,  0.01474423,  0.01545567,  0.01163002,  0.00443506, -0.0038142,
            -0.0104439,  -0.01333105, -0.01163274, -0.00607993,  0.00127966,  0.0078125,
            0.01124905,  0.01050454,  0.00605926, -0.00025205, -0.00596481, -0.00894244,
            -0.00819097, -0.00421012,  0.00125195,  0.00593078,  0.00795973,  0.00659377,
            0.00245907, -0.00275275, -0.00699729, -0.00869041, -0.00729189, -0.00344372,
            0.00135757,  0.00538664,  0.00734182,  0.00677075,  0.00413397,  0.00053042,
            -0.00276421, -0.0047482,  -0.00497581, -0.00360717, -0.00126124,  0.0012342,
            0.00309653,  0.00378171], dtype=np.float32)

    # Testing
    np.testing.assert_allclose(dobsf, output, atol=1.e-7)

if __name__ == "__main__" :
    np.testing.run_module_suite()
