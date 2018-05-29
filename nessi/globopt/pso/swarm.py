#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: swarm.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Class and methods for particle swarm optimization.

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

class Swarm():
    """
    Swarm
    """

    def __init__(self):
        """
        Initialize Swarm class
        """
        self.current = np.zeros((1, 1, 3), dtype=np.float32)
        self.velocity = np.zeros((1, 1, 3), dtype=np.float32)
        self.history = np.zeros((1, 1, 3), dtype=np.float32)
        self.misfit = np.zeros(1, dtype=np.float32)
        self.pspace = np.zeros((1, 1, 3), dtype=np.float32)

    def init_pspace(self, fmod):
        """
        Initialiaze parameter space from file

        :param fmod: input file containing the boundaries of the parameter space.
        """

        # Load pspace file in a temporary array
        tmp = np.loadtxt(fmod, ndmin=2, comments='#')

        # Check the number of points per particule
        npts = tmp.shape[0]
        npar = int(tmp.shape[1]/3)

        # Resize pspace array
        self.pspace.resize(npts, npar, 3)

        # Fill pspace array
        i = 0
        for ipar in range(0, npar):
            self.pspace[:, ipar, :] = tmp[:, i:i+3]
            i += 3

    def init_particles(self, nindv):
        """
        Initialize all the particles of the swarm.

        :param nindv: integer, number of particles
        """

        # Get npts and npar from pspace
        npts = self.pspace.shape[0]
        npar = self.pspace.shape[1]

        # Resize arrays
        self.current.resize(nindv, npts, npar)
        self.velocity.resize(nindv, npts, npar)
        self.history.resize(nindv, npts, npar)
        self.misfit.resize(nindv)

        # Random generation of particle position
        for indv in range(0, nindv):
            p_random = np.random.random_sample((npts, npar))
            self.current[indv, :, :] = self.pspace[:, :, 0]\
                + p_random*(self.pspace[:, :, 1]-self.pspace[:, :, 0])

    def _get_grid(self, ndim):
        """
        Define toroidal grid
        """
        nindv = self.current.shape[0]
        if nindv%ndim == 0:
            n1 = ndim
            n2 = int(nindv/ndim)
            vngrid = np.zeros((nindv, 4), dtype=np.int)
            for i2 in range(0, n2):
                for i1 in range(0, n1):
                    k = (i2*n1)+i1
                    # top
                    if i1 == 0:
                        vngrid[k, 0] = i2*n1+(n1-1)
                    else:
                        vngrid[k, 0] = i2*n1+(i1-1)
                    # right
                    if i2 == n2-1:
                        vngrid[k, 1] = i1
                    else:
                        vngrid[k, 1] = (i2+1)*n1+i1
                    # bottom
                    if i1 == n1-1:
                        vngrid[k, 2] = i2*n1
                    else:
                        vngrid[k, 2] = i2*n1+(i1+1)
                    # left
                    if i2 == 0:
                        vngrid[k, 3] = ((n2-1)*n1)+i1
                    else:
                        vngrid[k, 3] = (i2-1)*n1+i1
        else:
            raise ValueError('ndim must be a multiple of nindv')

        return vngrid

    def get_gbest(self, topology, indv=0, ndim=0):
        """
        Get gbest particle of the whole swarm or in the neighborhood of
        a given particle.
        """

        nindv = self.current.shape[0]

        # Get the best particle of the whole swarm
        if topology == 'full':
            ibest = np.argmin(self.misfit[:])

        # Get the best particle in the neighborhood (1 left, 1 right)
        # of the particle including itself.
        if topology == 'ring':
            ibest = indv
            vbest = self.misfit[indv]
            for i in range(indv-1, indv+2):
                ii = i
                if i < 0:
                    ii = nindv-1
                if i == nindv:
                    ii = 0
                if self.misfit[ii] < vbest:
                    ibest = ii
                    vbest = self.misfit[ii]

        # Get the best particle in the neighborhood (left, right, top, bottom)
        # of the particle including itself.
        if topology == 'toroidal':
            grid = self._get_grid(ndim)
            ibest = indv
            vbest = self.misfit[indv]
            for i in range(0, 4):
                if self.misfit[grid[indv, i]] < vbest:
                    ibest = grid[indv, i]
                    vbest = self.misfit[grid[indv, i]]

        return self.history[ibest, :, :]

    def update(self, **kwargs):
        """
        Standard PSO update.

        :param control: 0 for weight (default), 1 for constriction
        :param c_0: value of the control parameter (default 0.7298)
        :param c_1: value of the cognitive parameter (default 2.05)
        :param c_2: value of the social parameter (default 2.05)
        :param topology: used topology (default 'full'): full, ring, toroidal
        :param ndim: number of particles in the first dimension if toroidal topology is used
        """

        # Parse kwargs parameter list
        ctrl = kwargs.get('control', 0)
        omega = kwargs.get('c_0', 0.7298)
        topology = kwargs.get('topology', 'full')
        ndim = kwargs.get('ndim', 0)

        if ctrl == 0:
            cog = kwargs.get('c_1', 2.05)
            soc = kwargs.get('c_2', 2.05)
        if ctrl == 1:
            cog = omega*kwargs.get('c_1', 2.05)
            soc = omega*kwargs.get('c_2', 2.05)

        # Update process
        for indv in range(0, self.current.shape[0]):
            gbest = self.get_gbest(topology, indv, ndim)
            for ipts in range(0, self.pspace.shape[0]):
                for ipar in range(0, self.pspace.shape[1]):

                    # Get values
                    current = self.current[indv, ipts, ipar]
                    velocity = self.velocity[indv, ipts, ipar]
                    history = self.history[indv, ipts, ipar]

                    # Update velocity vector
                    self.velocity[indv, ipts, ipar] = omega*velocity\
                                                + cog*np.random.random_sample()\
                                                * (history-current)\
                                                + soc*np.random.random_sample()\
                                                * (gbest[ipts, ipar]-current)

                    # Check particle velocity
                    # vvv = particles[ibest]['history'][ipts,ipar]
                    if(np.abs(self.velocity[indv, ipts, ipar]) > self.pspace[ipts, ipar, 2]):
                        self.velocity[indv, ipts, ipar] = \
                            np.sign(self.velocity[indv, ipts, ipar])\
                            * self.pspace[ipts, ipar, 2]

                    # Update particle position
                    self.current[indv, ipts, ipar] += self.velocity[indv, ipts, ipar]

                    # Check if particle is in parameter space
                    if(self.current[indv, ipts, ipar] < self.pspace[ipts, ipar, 0]):
                        self.current[indv, ipts, ipar] = self.pspace[ipts, ipar, 0]
                    if(self.current[indv, ipts, ipar] > self.pspace[ipts, ipar, 1]):
                        self.current[indv, ipts, ipar] = self.pspace[ipts, ipar, 1]
