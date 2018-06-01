#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: test_windowing.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Test suite for the windowing functions (nessi.signal.windowing)

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
from nessi.signal.windowing import time_window
from nessi.signal.windowing import space_window

def test_time_window_one_trac():
    """
    signal.time_window for one-trace signal.
    """

    # Create initial data trace
    ns = 2048   # number of time sample
    dt = 0.0001 # time sampling
    dobs = np.zeros((ns), dtype=np.float32)

    # Define the window
    tmin = 0.01
    tmax = 0.20

    # Attempted number of time samples in the windowed signal
    nsw = int((tmax-tmin)/dt)+1

    # Windowing
    dobsw = time_window(dobs, tmin, tmax, dt)

    # Testing
    np.testing.assert_equal(len(dobsw), nsw)

def test_time_window_multi_trac_axis0():
    """
    signal.time_window for multi-trace signal.
    """

    # Create initial data trace
    ns = 2048   # number of time sample
    dt = 0.0001 # time sampling
    ntrac = 24
    dobs = np.zeros((ns, ntrac), dtype=np.float32)

    # Define the window
    tmin = 0.01
    tmax = 0.20

    # Attempted number of time samples in the windowed signal
    nsw = int((tmax-tmin)/dt)+1

    # Windowing
    dobsw = time_window(dobs, tmin, tmax, dt, axis=0)

    # Testing
    np.testing.assert_equal(np.size(dobsw, axis=0), nsw)

def test_time_window_multi_trac_axis1():
    """
    signal.time_window for multi-trace signal.
    """

    # Create initial data trace
    ns = 2048   # number of time sample
    dt = 0.0001 # time sampling
    ntrac = 24
    dobs = np.zeros((ntrac, ns), dtype=np.float32)

    # Define the window
    tmin = 0.01
    tmax = 0.20

    # Attempted number of time samples in the windowed signal
    nsw = int((tmax-tmin)/dt)+1

    # Windowing
    dobsw = time_window(dobs, tmin, tmax, dt, axis=1)

    # Testing
    np.testing.assert_equal(np.size(dobsw, axis=1), nsw)

def test_space_window_multi_trac_axis0():
    """
    signal.space_window for multi-trace signal.
    """

    # Create initial data trace
    ns = 2048   # number of time sample
    dt = 0.0001 # time sampling
    ntrac = 24
    dobs = np.zeros((ntrac, ns), dtype=np.float32)

    # Define the window
    imin = 5
    imax = 15

    # Attempted number of time samples in the windowed signal
    ntracw = imax-imin+1

    # Windowing
    dobsw = space_window(dobs, imin, imax, axis=0)

    # Testing
    np.testing.assert_equal(np.size(dobsw, axis=0), ntracw)

def test_space_window_multi_trac_axis1():
    """
    signal.space_window for multi-trace signal.
    """

    # Create initial data trace
    ns = 2048   # number of time sample
    dt = 0.0001 # time sampling
    ntrac = 24
    dobs = np.zeros((ns, ntrac), dtype=np.float32)

    # Define the window
    imin = 5
    imax = 15

    # Attempted number of time samples in the windowed signal
    ntracw = imax-imin+1

    # Windowing
    dobsw = space_window(dobs, imin, imax, axis=1)

    # Testing
    np.testing.assert_equal(np.size(dobsw, axis=1), ntracw)

if __name__ == "__main__" :
    np.testing.run_module_suite()
