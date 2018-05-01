#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 13:06:55 2018

@author: pageotd
"""
import numpy as np


def particles(nindv, npts, npar):
    """
    Particle
    """

    # Initialize
    particle_type = np.dtype([
        ('current', 'f4', (npts, npar)),
        ('velocity', 'f4', (npts, npar)),
        ('history', 'f4', (npts, npar)),
        ('misfit', 'f4')
        ])

    particle = np.zeros(nindv, dtype=particle_type)

    return particle
