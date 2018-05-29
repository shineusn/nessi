#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: test_swarm.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Test suite for the Swarm mathods (nessi.globopt)

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
from nessi.globopt import Swarm


def test_init_pspace_one_line():
    """
    swarm.init_pspace test for one point search.
    """

    # Attempted output
    output = np.zeros((1, 2, 3), dtype=np.float32)
    output[0,0,0] = -3.0
    output[0,0,1] = 3.0
    output[0,0,2] = 0.6
    output[0,1,0] = -3.0
    output[0,1,1] = 3.0
    output[0,1,2] = 0.6

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Testing the parameter space initialization
    np.testing.assert_equal(swarm.pspace, output)

def test_init_pspace_multi_line():
    """
    swarm.init_pspace test for multipoints search.
    """

    # Attempted output
    output = np.zeros((3, 2, 3), dtype=np.float32)
    output = np.array([
        [[-3.0, 3.0, 0.6],
         [-3.0, 3.0, 0.6]],
        [[-3.0, 3.0, 0.6],
         [-3.0, 3.0, 0.6]],
        [[-3.0, 3.0, 0.6],
         [-3.0, 3.0, 0.6]]
        ], dtype=np.float32)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_multi_line.txt')

    # Testing the parameter space initialization
    np.testing.assert_equal(swarm.pspace, output)

def test_init_particles():
    """
    swarm.init_particles test.
    """

    # Attempted output
    output = np.array([[[-0.49786797,  1.321947  ],
                        [-2.9993138 , -1.1860045 ],
                        [-2.1194646 , -2.4459684 ]],
                       [[-1.8824388 , -0.9266356 ],
                        [-0.61939514,  0.23290041],
                       [-0.4848329 ,  1.111317  ]]]
                      , dtype=np.float32)

    # Initialize the random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_multi_line.txt')

    # Initialize particles
    swarm.init_particles(2)

    # Testing particle initializations
    np.testing.assert_equal(swarm.current, output)

def test_get_gbest_full():
    """
    swarm.get_best tests.
    """

    # Attempted output
    output = np.array([[-0.4848329 ,  1.111317  ]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[:] = 1.0
    swarm.misfit[5] = 0.0

    # Testing get_gbest for topology: full
    np.testing.assert_equal(swarm.get_gbest(topology='full'), output)

def test_get_gbest_ring():
    """
    swarm.get_best tests.
    """

    # Attempted output
    output = np.array([[-0.4848329 ,  1.111317  ]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[:] = 1.0
    swarm.misfit[5] = 0.0

    # Testing get_gbest for topology: ring
    np.testing.assert_equal(swarm.get_gbest(topology='ring', indv=4), output)

def test_get_gbest_toroidal():
    """
    swarm.get_best tests.
    """

    # Attempted output
    output = np.array([[-0.4848329 ,  1.111317  ]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[:] = 1.0
    swarm.misfit[5] = 0.0

    # Testing get_gbest for topology: toroidal
    np.testing.assert_equal(swarm.get_gbest(topology='toroidal', indv=8, ndim=3), output)

def test_update_weight_full():
    """
    swarm.update with inertia weight and full topology options.
    """

    # Attempted output
    output = np.array([
            [[-1.09786797,  0.72194695]],
            [[-2.39931393, -1.78600454]],
            [[-2.11946464, -2.44596839]],
            [[-2.08705616, -1.52663565]],
            [[-1.21939516, -0.36709961]],
            [[-1.08483291,  0.51131701]],
            [[-2.3334105 ,  1.66870463]],
            [[-2.40458131,  0.42280507]],
            [[-1.09617114, -0.24786106]]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[0] = 1.00
    swarm.misfit[1] = 0.28
    swarm.misfit[2] = 0.01
    swarm.misfit[3] = 0.72
    swarm.misfit[4] = 0.53
    swarm.misfit[5] = 0.02
    swarm.misfit[6] = 0.64
    swarm.misfit[7] = 0.21
    swarm.misfit[8] = 0.98

    # Testing update method
    swarm.update(control=0, topology='full')
    np.testing.assert_equal(swarm.current, output)

def test_update_weight_ring():
    """
    swarm.update with inertia weight and ring topology options.
    """

    # Attempted output
    output = np.array([
            [[-1.09786797,  0.72194695]],
            [[-2.39931393, -1.78600454]],
            [[-2.11946464, -2.44596839]],
            [[-2.08705616, -1.52663565]],
            [[-0.53235936,  0.8329004 ]],
            [[-0.48483291,  1.11131704]],
            [[-1.17328644,  1.66870463]],
            [[-2.83567452,  1.02280509]],
            [[-1.09617114,  0.7172299 ]]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[0] = 1.00
    swarm.misfit[1] = 0.28
    swarm.misfit[2] = 0.01
    swarm.misfit[3] = 0.72
    swarm.misfit[4] = 0.53
    swarm.misfit[5] = 0.02
    swarm.misfit[6] = 0.64
    swarm.misfit[7] = 0.21
    swarm.misfit[8] = 0.98

    # Testing update method
    swarm.update(control=0, topology='ring')
    np.testing.assert_equal(swarm.current, output)

def test_update_weight_toroidal():
    """
    swarm.update with inertia weight and toroidal topology options.
    """

    # Attempted output
    output = np.array([
            [[-1.09786797,  0.72194695]],
            [[-2.39931393, -1.78600454]],
            [[-2.11946464, -2.44596839]],
            [[-1.28243876, -0.3266356 ]],
            [[-0.53235936,  0.8329004 ]],
            [[-1.08483291,  0.51131701]],
            [[-2.37328649,  1.66870463]],
            [[-2.83567452,  1.02280509]],
            [[-1.09617114, -0.24786106]]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[0] = 1.00
    swarm.misfit[1] = 0.28
    swarm.misfit[2] = 0.01
    swarm.misfit[3] = 0.72
    swarm.misfit[4] = 0.53
    swarm.misfit[5] = 0.02
    swarm.misfit[6] = 0.64
    swarm.misfit[7] = 0.21
    swarm.misfit[8] = 0.98

    # Testing update method
    swarm.update(control=0, topology='toroidal', ndim=3)
    np.testing.assert_equal(swarm.current, output)

def test_update_constriction_full():
    """
    swarm.update with constriction and full topology options.
    """

    # Attempted output
    output = np.array([
            [[-0.97847301,  0.72194695]],
            [[-2.39931393, -1.78600454]],
            [[-2.11946464, -2.44596839]],
            [[-2.03176856, -1.52663565]],
            [[-1.21939516, -0.36709961]],
            [[-1.08483291,  0.51131701]],
            [[-2.18206501,  1.66870463]],
            [[-2.52106285,  0.42280507]],
            [[-1.09617114, -0.24786106]]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[0] = 1.00
    swarm.misfit[1] = 0.28
    swarm.misfit[2] = 0.01
    swarm.misfit[3] = 0.72
    swarm.misfit[4] = 0.53
    swarm.misfit[5] = 0.02
    swarm.misfit[6] = 0.64
    swarm.misfit[7] = 0.21
    swarm.misfit[8] = 0.98

    # Testing update method
    swarm.update(control=1, topology='full')
    np.testing.assert_equal(swarm.current, output)

def test_update_constriction_ring():
    """
    swarm.update with constriction and ring topology options.
    """

    # Attempted output
    output = np.array([
            [[-1.09786797,  0.72194695]],
            [[-2.39931393, -1.78600454]],
            [[-2.11946464, -2.44596839]],
            [[-2.03176856, -1.52663565]],
            [[-0.55587643,  0.8329004 ]],
            [[-0.48483291,  1.11131704]],
            [[-1.17328644,  1.66870463]],
            [[-2.83567452,  1.02280509]],
            [[-1.09617114,  0.61858237]]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[0] = 1.00
    swarm.misfit[1] = 0.28
    swarm.misfit[2] = 0.01
    swarm.misfit[3] = 0.72
    swarm.misfit[4] = 0.53
    swarm.misfit[5] = 0.02
    swarm.misfit[6] = 0.64
    swarm.misfit[7] = 0.21
    swarm.misfit[8] = 0.98

    # Testing update method
    swarm.update(control=1, topology='ring')
    np.testing.assert_equal(swarm.current, output)

def test_update_constriction_toroidal():
    """
    swarm.update with constriction and toroidal topology options.
    """

    # Attempted output
    output = np.array([
            [[-0.97847301,  0.72194695]],
            [[-2.39931393, -1.78600454]],
            [[-2.11946464, -2.44596839]],
            [[-1.28243876, -0.3266356 ]],
            [[-0.55587643,  0.8329004 ]],
            [[-1.08483291,  0.51131701]],
            [[-2.37328649,  1.66870463]],
            [[-2.83567452,  1.02280509]],
            [[-1.09617114, -0.24786106]]], dtype=np.float32)

    # Initialize random number generator
    np.random.seed(1)

    # Initialize the swarm class
    swarm = Swarm()

    # Initialize the parameter space
    swarm.init_pspace('data/pspace_one_line.txt')

    # Initialize particles
    swarm.init_particles(9)

    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[0] = 1.00
    swarm.misfit[1] = 0.28
    swarm.misfit[2] = 0.01
    swarm.misfit[3] = 0.72
    swarm.misfit[4] = 0.53
    swarm.misfit[5] = 0.02
    swarm.misfit[6] = 0.64
    swarm.misfit[7] = 0.21
    swarm.misfit[8] = 0.98

    # Testing update method
    swarm.update(control=1, topology='toroidal', ndim=3)
    np.testing.assert_equal(swarm.current, output)

if __name__ == "__main__" :
    np.testing.run_module_suite()
