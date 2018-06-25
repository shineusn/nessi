#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: genalg.py
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

class Genalg():
    """
    Genetic Algorithm class
    """

    def __init__(self):
        """
        Initialize Genalg class.
        """
        # Array to store the lenght of each gene
        self.clenght = np.zeros(1, dtype=np.int16)
        # Array to store chromosomes
        self.current = np.zeros(1, dtype=np.int16)
        # Array to store the misfit for each chromosome
        self.misfit = np.zeros(1, dtype=np.float32)
        # Array to store the parameter space
        self.pspace = np.zeros((1, 1, 3), dtype=np.float32)

    def init_pspace(self, fmod):
        """
        Initialiaze parameter space from file

        :param fmod: input file containing the boundaries of the parameter space.
        """

        # Load pspace file in a temporary array
        tmp = np.loadtxt(fmod, ndmin=2, comments='#')

        # Check the number of points per chromosome
        npts = tmp.shape[0]

        # Check the number of parameter per points
        npar = int(tmp.shape[1]/3)

        # Resize pspace array
        self.pspace.resize(npts, npar, 3)

        # Fill pspace array
        i = 0
        for ipar in range(0, npar):
            self.pspace[:, ipar, :] = tmp[:, i:i+3]
            i += 3

    def _power2(self, n):
        """
        Search the closest power of 2 of an integer value.
        """
        n2 = int(2)
        while(n2 < n):
            n2 *= int(2)
        return n2

    def _binstrlen(self, n):
        """
        Return the maximum lenght of a bit-string given n (power of 2).
        """
        npw = self._power2(n)
        l = 1./np.log(2.)*np.log(float(npw))
        return int(round(l))

    def _encoding(self, x, lb, ub, nx):
        """
        Convert real value in its binary representation given boundaries
        and discretization (power of 2).

        :param x: value between lb and ub
        :param lb: lower bound value
        :param ub: upper bound value
        :param nx: number of discrete samples
        """

        # Convert x value to integer
        ix = int(round(float(nx-1)*(x-lb)/(ub-lb)))

        # Get the gene length
        l = self._binstrlen(nx)

        # Initialize the gene
        gene = np.zeros((l), dtype=np.int8)
        tmp = ix

        # Fill the gene with 0 and/or 1
        for i in range(0, l):
            gene[l-1-i] = tmp%2
            tmp = tmp//2

        return gene

    def _decoding(self, b, lb, ub, nx):
        """
        Convert binary reprensentation in real value given boundaries
        and discretization (power of 2).

        :param b: binary code
        :param lb: lower bound
        :param ub: upper bound
        :param nx: number of discrete samples
        """

        # Get sampling
        dx = (ub-lb)/float(nx-1)

        # Get the gene's lenght
        l = self._binstrlen(nx)

        # Loop over bytes
        ix = 0
        for i in range(0, l):
            ix += b[l-1-i]*(2**i)

        # Calculate final value
        x = lb+float(ix)*dx

        return x

    def chromolenght(self):
        """
        Calculate the lenght in byte of each gene of the chromosomes
        """

        # Get the number of points and the number of parameters per point
        npts = self.pspace.shape[0]
        npar = self.pspace.shape[1]

        # Initialize clenght array
        self.clenght = np.zeros(npts*npar, dtype=np.int16)

        # Loop over points and parameters
        for ipts in range(0, npts):
            for ipar in range(0, npar):
                # Check value
                if self.pspace[ipts, ipar, 2] > 1:
                    self.clenght[ipts*(npar-1)+ipar] = self._binstrlen(self.pspace[ipts, ipar, 2])
                else:
                    self.clenght[ipts*(npar-1)+ipar] = 1

    def chromowrite(self, rmod):
        """
        Write model parameters in binary form.

        :param rmod: array (npts, npar) of random parameters
        """

        # length of chromosome
        nbin = np.sum(self.clenght)

        # Number of points and parameters
        npts = rmod.shape[0]
        npar = rmod.shape[1]

        # population array
        chromo = np.zeros(nbin, dtype=np.int16)

        l = 0
        i = 0

        # Loop over points
        for ipts in range(0, npts):
            # Loop over parameters
            for ipar in range(0, npar):
                xmin = self.pspace[ipts, ipar, 0]
                xmax = self.pspace[ipts, ipar, 1]
                xsmp = self.pspace[ipts, ipar, 2]
                if(xsmp == 1):
                    chromo[l:l+1] = 0
                    l += 1
                else:
                    a = self.clenght[i]
                    x = rmod[ipts, ipar]
                    chromo[l:l+a] = self._encoding(x, xmin, xmax, xsmp)
                    l += a
                i += 1

        return chromo

    def chromoread(self, bmod):
        """
        Read binary representation and translate in term of real-value
        parameters.

        :param bmod: chromosome
        """

        # Get the numner of points and the number of parameter per points
        npts = self.pspace.shape[0]
        npar = self.pspace.shape[1]

        # Initialize output model
        model = np.zeros((npts, npar), dtype=np.float32)

        # Get the real value model from genes
        i=-1
        for ipts in range(0, npts):
            for ipar in range(0, npar):
                i+=1
                pmin = self.pspace[ipts, ipar, 0]
                pmax = self.pspace[ipts, ipar, 1]
                psmp = self.pspace[ipts, ipar, 2]
                if(i == 0):
                    igmin = 0
                    igmax = self.clenght[ipar]
                else:
                    igmin += self.clenght[i-1]
                    igmax += self.clenght[i]

                if psmp > 1:
                    model[ipts, ipar] = self._decoding(bmod[igmin:igmax], pmin, pmax, psmp)
                else:
                    model[ipts, ipar] = pmin

        return model

    def init_chromosome(self, nindv, ncvt=0):
        """
        Initialize chromosome population.

        :param nindv: number of individuals/chromosomes in the pool.
        :param ncvt: integer, number of iteration for centroidal Voronoi tessellation (McQueen algorithm)
        """

        # Get the number of points and the number of parameters per points
        npts = self.pspace.shape[0]
        npar = self.pspace.shape[1]

        # Get the gene lenghts
        self.chromolenght()

        # Get the total chromosome lenght
        lenght = np.sum(self.clenght)

        # Initialize population
        self.current = np.zeros((nindv, lenght), dtype=np.int16)
        self.misfit = np.zeros(nindv, dtype=np.float32)

        # Initiliaze random model
        rmod = np.zeros((npts, npar), dtype=np.float32)

        # Loop over individuals
        for indv in range(0, nindv):
            # Loop over points and parameters
            for ipts in range(0, npts):
                for ipar in range(0, npar):
                    vmin = self.pspace[ipts, ipar, 0]
                    vmax = self.pspace[ipts, ipar, 1]
                    nv = self.pspace[ipts, ipar, 2]
                    if nv > 1:
                        # Randomize
                        r = np.random.randint(0, high=nv)
                        rmod[ipts, ipar] = vmin+r*(vmax-vmin)/float(nv-1)
                    else:
                        rmod[ipts, ipar] = vmin
            # Write genes in chromosomes
            self.current[indv, :] = self.chromowrite(rmod)

        # CVT
        if ncvt > 0:
            # Initialize
            j = np.zeros(nindv, dtype=np.float32)
            j[:] = 1.
            # Create temporary particle array
            qtmp = np.zeros((npts, npar), dtype=np.float32)
            # Loop over iterations
            for it in range(0, ncvt):
                # Random individual
                for ipts in range(0, npts):
                    for ipar in range(0, npar):
                        vmin = self.pspace[ipts, ipar, 0]
                        vmax = self.pspace[ipts, ipar, 1]
                        nv = self.pspace[ipts, ipar, 2]
                        if nv > 1:
                            # Randomize
                            r = np.random.randint(0, high=nv)
                            qtmp[ipts, ipar] = vmin+r*(vmax-vmin)/float(nv-1)
                        else:
                            qtmp[ipts, ipar] = vmin
                # Calculate distance
                d = np.zeros(nindv, dtype=np.float32)
                for indv in range(0, nindv):
                    qpool = self.chromoread(self.current[indv,:])
                    for ipts in range(0,npts):
                        for ipar in range(0, npar):
                            d[indv] += ((qpool[ipts,ipar]-qtmp[ipts,ipar])/
                                self.pspace[ipts,ipar,1])**2
                d[:] = np.sqrt(d[:])
                # Search closest individual
                iclose = np.argmin(d)
                # Correct position
                qpool = self.chromoread(self.current[iclose,:])
                for ipts in range(0, npts):
                    for ipar in range(0, npar):
                        qpool[ipts,ipar] = (j[iclose]*qpool[ipts,ipar]+qtmp[ipts,ipar])/(j[iclose]+1.)
                self.current[iclose, :] = self.chromowrite(qpool)
                j[iclose] += 1.

    def tournament(self, k, nelit):
        """
        K-way tournament selection.
        """

        # Get the number of chromosomes and the lenght of chromosomes
        nindv = self.current.shape[0]
        lenght = self.current.shape[1]

        # Initialize selected parents array
        selected = np.zeros((nindv, lenght), dtype=np.int16)

        # If elits
        if nelit > 0:
            # Copy misfit array
            misfit = np.zeros(nindv, dtype=np.float32)
            misfit[:] = self.misfit[:]
            # Loop over nelit
            for indv in range(0, nelit):
                ibest = np.argmin(misfit)
                selected[indv, :] = self.current[ibest, :]
                misfit[ibest] = np.amax(misfit)*10.

        # Loop over individuals
        for indv in range(nelit, nindv):
            # Loop over K
            for i in range(0, k):
                # Select competitor
                itest = np.random.randint(0, high=nindv)
                # Test competitor
                if i == 0:
                    ibest = itest
                    fbest = self.misfit[ibest]
                else:
                    if self.misfit[itest] < fbest:
                        ibest = itest
                        fbest = self.misfit[ibest]
            selected[indv, :] = self.current[ibest, :]

        return selected

    def crossover(self, selected, xtype, pc, nelit):
        """
        Cross-over operator.
        """

        # Get the number of chromosomes and the lenght of chromosomes
        nindv = self.current.shape[0]
        lenght = self.current.shape[1]

        # Initialize crossed offspring array
        crossed = np.zeros((nindv, lenght), dtype=np.int16)

        # If elits
        if nelit > 0:
            for indv in range(0, nelit):
                crossed[indv, :] = selected[indv, :]

        # Loop over individuals
        for indv in range(nelit, nindv, 2):
            # Check if cross-over or not
            if np.random.random_sample() < pc:
                # Cross-over point
                ic = np.random.randint(0, high=lenght)
                crossed[indv, :ic] = selected[indv, :ic]
                crossed[indv, ic:] = selected[indv+1, ic:]
                crossed[indv+1, :ic] = selected[indv+1, :ic]
                crossed[indv+1, ic:] = selected[indv, ic:]
            else:
                crossed[indv, :] = selected[indv, :]
                crossed[indv+1, :] = selected[indv+1, :]

        return crossed

    def mutation(self, crossed, mtype, pm, nelit):
        """
        Mutation operator.
        """

        # Get the number of chromosomes and the lenght of chromosomes
        nindv = self.current.shape[0]
        lenght = self.current.shape[1]

        # Get the number of genes
        ngene = len(self.clenght)

        # Initialize mutated offspring array
        mutated = np.zeros((nindv, lenght), dtype=np.int16)

        # If elits
        for indv in range(0, nelit):
            mutated[indv, :] = crossed[indv, :]

        # Loop over individuals
        for indv in range(nelit, nindv):
            # Loop over genes
            icount = 0
            for igene in range(0, ngene):
                # Loop over bits
                for ibit in range(0, self.clenght[igene]):
                    # Test Mutation
                    if np.random.random_sample() < pm:
                        if crossed[indv, icount] == 0:
                            mutated[indv, icount] = 1
                        else:
                            mutated[indv, icount] = 0
                    else:
                        mutated[indv, icount] = crossed[indv, icount]
                    icount += 1

        return mutated

    def update(self, stype='tournament', k=4, xtype='single', pc=0.5, mtype='simple', pm=0.2, nelit=0):
        """
        Update chromosomes using k-way tournament selection, single cross-over and simple mutation.
        """

        # Selection
        if stype == 'tournament':
            selected = self.tournament(k, nelit)

        # Cross-over
        if xtype == 'single':
            crossed = self.crossover(selected, xtype, pc, nelit)

        # Mutation
        if mtype == 'simple':
            mutated = self.mutation(crossed, mtype, pm, nelit)

        self.current[:, :] = mutated[:, :]
