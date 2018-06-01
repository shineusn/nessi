#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: filtering.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Data filtering functions.

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

def sin2filter(dobs, freq, amps, dt, axis=0):
    """
    Applies a zero-phase, sine-squared tapered filter (adapted from the
    sufilter command - Seismic Unix 44R1).

    :param dobs: --
    :param freq: array of filter frequencies (Hz)
    :param amps: array of filter amplitudes
    :param dt: time sampling
    :param axis: time axis if dobs is a 2D array
    """


    # Get number of time samples and numner of traces
    if np.ndim(dobs) == 1:
        ns = np.size(dobs)
        ntrac = 1
    else:
        if axis == 0:
            ns = np.size(dobs, axis=0)
            ntrac = np.size(dobs, axis=1)
        if axis == 1:
            ns = np.size(dobs, axis=1)
            ntrac = np.size(dobs, axis=0)

    # Calculate the Nyquist frequency
    fnyq = 0.5/dt

    # Fast Fourier transform
    gobs = np.fft.rfft(dobs, axis=axis)
    nfft = np.size(gobs, axis=axis)
    ftmp = np.fft.rfftfreq(nfft, dt)
    df = ftmp[1]


    # Create a gobs filter array
    if np.ndim(dobs) == 1:
        gobsfilter = np.zeros(nfft, dtype=np.complex64)
    else:
        gobsfilter = np.zeros((nfft, ntrac), dtype=np.complex64)

    # Get the number of filter frequencies
    npoly = len(freq)

    # Integer filter frequencies
    intfreq = np.zeros(npoly, dtype=np.int)
    for ipoly in range(0, npoly):
        intfreq[ipoly] = np.argmin(np.abs(ftmp-freq[ipoly]))

    # Initialize the polygonal filter with sin^2 tapering
    pfilt = np.zeros(nfft, dtype=np.complex64)

    # From 0 to first filter frequency
    for ifreq in range(0, intfreq[0]):
        pfilt[ifreq] = amps[0]

    # Middle frequencies
    for ipoly in range(0, npoly-1):

        if amps[ipoly] < amps[ipoly+1]:
            for ifreq in range(intfreq[ipoly], intfreq[ipoly+1]):
                c = 0.5*np.pi/float(intfreq[ipoly+1]-intfreq[ipoly]+2)
                s = np.sin(c*float(ifreq-intfreq[ipoly]+1))
                a = amps[ipoly+1]-amps[ipoly]
                pfilt[ifreq] = amps[ipoly]+a*s*s

        if amps[ipoly] > amps[ipoly+1]:
            for ifreq in range(intfreq[ipoly], intfreq[ipoly+1]):
                c = 0.5*np.pi/float(intfreq[ipoly+1]-intfreq[ipoly]+2)
                s = np.sin(c*float(intfreq[ipoly]-ifreq+1))
                a = amps[ipoly]-amps[ipoly+1]
                pfilt[ifreq] = amps[ipoly+1]+a*s*s

        if amps[ipoly] == amps[ipoly+1]:
            for ifreq in range(intfreq[ipoly], intfreq[ipoly+1]):
                pfilt[ifreq] = amps[ipoly]

    # From the last filter frequency to the last frequency
    for ifreq in range(intfreq[-1], nfft):
        pfilt[ifreq] = amps[-1]

    # Apply filter
    if np.ndim(dobs) == 1:
        gobsfilter[:] = gobs[:]*pfilt[:]
        dobsfilter = np.fft.irfft(gobsfilter, n=ns)
    else:
        if axis == 0:
            for itrac in range(0, ntrac):
                gobsfilter[:, itrac] = gobs[:, itrac]*pfilt[:]
            dobsfilter = np.fft.irfft(gobsfilter, n=ns, axis=0)

        if axis == 1:
            for itrac in range(0, ntrac):
                gobsfilter[itrac, :] = gobs[itrac,:]*pfilt[:]
            dobsfilter = np.fft.irfft(gobsfilter, n=ns, axis=1)

    return dobsfilter
