#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: test_genalg.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Test suite for the Genetic Algorithm methods (nessi.globopt)

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
from nessi.globopt import Genalg

def test_init_pspaceGA_one_line():
    """
    genalg.init_pspace test for one point search.
    """

    # Attempted output
    output = np.zeros((1, 2, 3), dtype=np.float32)
    output[0,0,0] = -3.0
    output[0,0,1] = 3.0
    output[0,0,2] = 8
    output[0,1,0] = -3.0
    output[0,1,1] = 3.0
    output[0,1,2] = 8

    # Initialize the swarm class
    genalg = Genalg()

    # Initialize the parameter space
    genalg.init_pspace('data/pspaceGA_one_line.txt')

    # Testing the parameter space initialization
    np.testing.assert_equal(genalg.pspace, output)

def test_init_pspaceGA_multi_line():
    """
    genalg.init_pspace test for multipoints search.
    """

    # Attempted output
    output = np.zeros((3, 2, 3), dtype=np.float32)
    output = np.array([
            [[-3.0, 3.0, 8.], [-3.0, 3.0, 8.]],
            [[-3.0, 3.0, 8.], [-3.0, 3.0, 8.]],
            [[-3.0, 3.0, 8.], [-3.0, 3.0, 8.]]], dtype=np.float32)

    # Initialize the swarm class
    genalg = Genalg()

    # Initialize the parameter space
    genalg.init_pspace('data/pspaceGA_multi_line.txt')

    # Testing the parameter space initialization
    np.testing.assert_equal(genalg.pspace, output)

def test_chromolenght():
    """
    genalg.init_chromosome test.
    """

    # Attempt output
    output = np.array([3, 3], dtype=np.int16)

    # Initialize the swarm class
    genalg = Genalg()

    # Initialize the parameter space
    genalg.init_pspace('data/pspaceGA_one_line.txt')

    # Initialize chromosome lenght
    genalg.chromolenght()

    # Testing
    np.testing.assert_equal(genalg.clenght, output)

def test_encoding():
    """
    genalg._encoding test
    """

    # Attempt output
    output = np.array([1, 0, 1], dtype=np.int16)

    # Initialize the Genetic Algorithm class
    genalg = Genalg()

    # Initialize random number generator
    np.random.seed(1)

    # Define boundaries, number of samples and the value to convert
    lb = -3.0
    ub = 3.0
    nx = 8
    r = np.random.randint(0, high=nx)
    x =  lb+r*(ub-lb)/float(nx-1)

    # Testing
    bcode = genalg._encoding(x, lb, ub, nx)

    # Testing
    np.testing.assert_equal(bcode, output)

def test_decoding():
    """
    genalg._decoding test
    """

    # Binary input
    b = np.array([1, 0, 1], dtype=np.int16)

    # Initialize the Genetic Algorithm class
    genalg = Genalg()

    # Initialize random number generator
    np.random.seed(1)

    # Define boundaries, number of samples and the value to convert
    lb = -3.0
    ub = 3.0
    nx = 8
    r = np.random.randint(0, high=nx)
    x =  lb+r*(ub-lb)/float(nx-1)

    # Testing
    vcode = genalg._decoding(b, lb, ub, nx)

    # Testing
    np.testing.assert_equal(vcode, x)


def test_chromowrite():
    """
    genalg.chromowrite test.
    """

    # Attempt output
    output = np.array([1, 0, 1, 0, 1, 1], dtype=np.int16)

    # Initialize the random number generator
    np.random.seed(1)

    # Initialize the swarm class
    genalg = Genalg()

    # Initialize the parameter space
    genalg.init_pspace('data/pspaceGA_one_line.txt')

    # Get number of points and number of parameters per point
    npts = genalg.pspace.shape[0]
    npar = genalg.pspace.shape[1]

    # Get the legnht of chromosome
    genalg.chromolenght()

    # Initialize real value model
    rmod = np.zeros((npts, npar), dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Random value from pspace
    for ipts in range(0, npts):
        for ipar in range(0, npar):
            pmin = genalg.pspace[ipts, ipar, 0]
            pmax = genalg.pspace[ipts, ipar, 1]
            delt = int(genalg.pspace[ipts, ipar, 2])
            r = np.random.randint(0, high=delt)
            rmod[ipts, ipar] = pmin+r*(pmax-pmin)/float(delt-1)

    # Testing
    chromosome = genalg.chromowrite(rmod)

    np.testing.assert_equal(chromosome, output)

    #array([[ 1.2857143 , -0.42857143]], dtype=float32)

def test_chromoread():
    """
    genalg.chromoread test
    """

    # Input chromosome
    chromosome = np.array([1, 0, 1, 0, 1, 1], dtype=np.int16)

    # Attempt output
    output = np.array([[ 1.2857143 , -0.42857143]], dtype=np.float32)

    # Initialize the random number generator
    np.random.seed(1)

    # Initialize the swarm class
    genalg = Genalg()

    # Initialize the parameter space
    genalg.init_pspace('data/pspaceGA_one_line.txt')

    # Get number of points and number of parameters per point
    npts = genalg.pspace.shape[0]
    npar = genalg.pspace.shape[1]

    # Get the legnht of chromosome
    genalg.chromolenght()

    # Testing
    model = genalg.chromoread(chromosome)
    np.testing.assert_equal(model, output)


def test_init_chromosome():
    """
    genalg.init_chromosome test.
    """

    # Attempt output
    output = np.array([
        [1, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0]], dtype=np.int16)

    # Initialize the random number generator
    np.random.seed(1)

    # Initialize the swarm class
    genalg = Genalg()

    # Initialize the parameter space
    genalg.init_pspace('data/pspaceGA_one_line.txt')

    # Initialize chromosome lenght
    genalg.init_chromosome(2)

    # Testing
    np.testing.assert_equal(genalg.current[:,:], output)

if __name__ == "__main__" :
    np.testing.run_module_suite()
