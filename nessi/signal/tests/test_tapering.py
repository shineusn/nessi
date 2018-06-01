#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: test_tapering.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Test suite for the tapering functions (nessi.signal.tapering)

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
from nessi.signal.tapering import taper1d

def test_taper1d_linear():
    """
    signal.tapering.taper1d testing for linear taper.
    """

    # Create initial data trace
    ns = 128   # number of time sample
    dobs = np.zeros((ns), dtype=np.float32)
    dobs[:] = 1.

    # Define the taper
    ntap1 = 16
    ntap2 = 16

    # Tapering
    dobst = taper1d(dobs, ntap1, ntap2, type='linear')

    # Attempted output
    output = np.array([0.    , 0.0625, 0.125 , 0.1875, 0.25  , 0.3125, 0.375 , 0.4375,
       0.5   , 0.5625, 0.625 , 0.6875, 0.75  , 0.8125, 0.875 , 0.9375,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    , 1.    ,
       0.9375, 0.875 , 0.8125, 0.75  , 0.6875, 0.625 , 0.5625, 0.5   ,
       0.4375, 0.375 , 0.3125, 0.25  , 0.1875, 0.125 , 0.0625, 0.    ],
      dtype=np.float32)

    # Testing
    np.testing.assert_allclose(dobst, output, atol=1.e-4)

def test_taper1d_sine():
    """
    signal.tapering.taper1d testing for sine taper.
    """

    # Create initial data trace
    ns = 128   # number of time sample
    dobs = np.zeros((ns), dtype=np.float32)
    dobs[:] = 1.

    # Define the taper
    ntap1 = 16
    ntap2 = 16

    # Tapering
    dobst = taper1d(dobs, ntap1, ntap2, type='sine')

    # Attempted output
    output = np.array([0.        , 0.09801714, 0.19509032, 0.29028466, 0.38268343,
       0.47139674, 0.55557024, 0.6343933 , 0.70710677, 0.77301043,
       0.8314696 , 0.8819213 , 0.9238795 , 0.95694035, 0.98078525,
       0.9951847 , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 0.9951847 , 0.98078525, 0.95694035,
       0.9238795 , 0.8819213 , 0.8314696 , 0.77301043, 0.70710677,
       0.6343933 , 0.55557024, 0.47139674, 0.38268343, 0.29028466,
       0.19509032, 0.09801714, 0.        ], dtype=np.float32)

    # Testing
    np.testing.assert_allclose(dobst, output, atol=1.e-4)

def test_taper1d_cosine():
    """
    signal.tapering.taper1d testing for cosine taper.
    """

    # Create initial data trace
    ns = 128   # number of time sample
    dobs = np.zeros((ns), dtype=np.float32)
    dobs[:] = 1.

    # Define the taper
    ntap1 = 16
    ntap2 = 16

    # Tapering
    dobst = taper1d(dobs, ntap1, ntap2, type='cosine')

    # Attempted output
    output = np.array([0.        , 0.00960736, 0.03806023, 0.08426519, 0.14644662,
       0.22221488, 0.30865827, 0.40245485, 0.5       , 0.59754515,
       0.6913417 , 0.7777851 , 0.8535534 , 0.9157348 , 0.96193975,
       0.9903926 , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 0.9903926 , 0.96193975, 0.9157348 ,
       0.8535534 , 0.7777851 , 0.6913417 , 0.59754515, 0.5       ,
       0.40245485, 0.30865827, 0.22221488, 0.14644662, 0.08426519,
       0.03806023, 0.00960736, 0.        ], dtype=np.float32)

    # Testing
    np.testing.assert_allclose(dobst, output, atol=1.e-4)

if __name__ == "__main__" :
    np.testing.run_module_suite()
