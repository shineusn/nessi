#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: subvalley_inversion.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Inversion of Rayleigh dispersion diagrams using PSO.

:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI

from nessi.io import SUdata
from nessi.pso import Swarm
from nessi.grd import sibson2

from seismod import seismod

def vsnu2vp(vsmod, numod):
    vpmod = np.sqrt(vsmod*vsmod*2.*(1.-numod)/(1.-2.*numod))
    return vpmod

# ------------------------------------------------------------------
# >> Initialize MPI
# ------------------------------------------------------------------

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


# ------------------------------------------------------------------
# >> Reference data
# ------------------------------------------------------------------

# One reference data is assigned to each slave.
if rank != 0:
    sufile = 'data/dobsz'+str(rank-1).zfill(2)+'.su'
    dobsz = SUdata()
    dobsz.read(sufile)


# ------------------------------------------------------------------
# >> Get information from SU header
# ------------------------------------------------------------------

# Get the source and receiver positions from SU headers.
if rank != 0:

    # Get scale for coordinates
    scalco = dobsz.header[0]['scalco']
    if scalco < 0:
        scale = -1./float(scalco)
    else:
        scale = float(scalco)

    # Get the source position
    sx = dobsz.header[0]['sx']*scale
    sz = dobsz.header[0]['sy']*scale

    # Get the receiver line
    nrec = len(dobsz.header)
    acq = np.zeros((nrec, 2), dtype=np.float32)
    for ir in range(0, nrec):
        acq[ir, 0] = dobsz.header[ir]['gx']*scale
        acq[ir, 1] = dobsz.header[ir]['gy']*scale


# >> Get time sampling
if rank != 0:
    ns = dobsz.header[0]['ns']
    dts = dobsz.header[0]['dt']/1000000.
    tmax = float(ns-1)*dts


# ------------------------------------------------------------------
# >> Define modeling parameters
# ------------------------------------------------------------------


    # >> Run parameters
    runpar = {'name': 'subvalley',
              'tmax': tmax, 'dt': 0.0001, # Time marching
              'snap': 0, 'dtsnap': 0.001}   # Snapshots

    # >> Model grid parameters
    modpar = {'n1': 51, 'n2': 301, 'dh': 0.5, # Grid dimensions
              'ifsurf': 1, 'npml': 20, 'apml': 1200., 'ppml': 8} # Boundary conditions

    # >> Acquisition parameters
    acqpar = {'sx': sx, 'sy': sz, # Source parameters
              'f0': 15., 't0': 0.1, 'spread': -1, 'type': 2,
              'acquisition': acq, 'dts': dts} # Receiver file name and data sampling


# ------------------------------------------------------------------
# >> Reference dispersion diagrams
# ------------------------------------------------------------------

# Calculating the reference dispersion diagrams using the MASW method
if rank != 0:
    disp = dobsz.masw(vmin=200., vmax=1200., dv=5., fmin=10., fmax=50.)
    disp /= np.amax(disp)

# Block until all processes have reached this point.
comm.Barrier()


# ------------------------------------------------------------------
# >> Initialize the swarm
# ------------------------------------------------------------------

# Initialize the number of generations and particles on master
# and slaves.
ngen = 10
nindv = 9 #49

# Initialize the swarm on the master only.
if rank == 0:
    swarm = Swarm()
    swarm.init_pspace('input/random_models.ascii')
    swarm.init_particles(nindv)


# ------------------------------------------------------------------
# >> First evaluation
# ------------------------------------------------------------------

# Initialize velocity and density models on slaves
if rank != 0:
    vpmod = np.zeros((51, 301), dtype=np.float32)
    vsmod = np.zeros((51, 301), dtype=np.float32)
    romod = np.zeros((51, 301), dtype=np.float32)

# Loop over particles
for indv in range(0, nindv):

    # Coarse to fine grid
    if rank == 0:
        npts = swarm.pspace.shape[0]
        xp = swarm.current[indv, :, 0]
        zp = swarm.current[indv, :, 1]
        # S-wave velocity model
        val = swarm.current[indv, :, 2]
        vsmod = sibson2(npts, xp, zp, val, 51, 301, 0.5)
        # Density model
        val = swarm.current[indv, :, 3]
        romod = sibson2(npts, xp, zp, val, 51, 301, 0.5)
        # Poisson's ratio model
        val = swarm.current[indv, :, 4]
        numod = sibson2(npts, xp, zp, val, 51, 301, 0.5)
        # P-wave velocity model
        vpmod = vsnu2vp(vsmod, numod)

    # Broadcast velocity and density models to slaves.
    comm.Bcast([vpmod, MPI.FLOAT], root=0)
    comm.Bcast([vsmod, MPI.FLOAT], root=0)
    comm.Bcast([romod, MPI.FLOAT], root=0)

    # Calculate observed data and evaluate
    if rank != 0:
        # Seismic modeling
        dcalz = seismod(runpar, modpar, acqpar, vpmod, vsmod, romod)
        # Rayleigh dispersion
        disp1 = dcalz.masw(vmin=200., vmax=1200., dv=5., fmin=10., fmax=50.)
        disp1 /= np.amax(disp1)
        # L2-norm
        L2 = 0.
        for iv in range(0, disp.shape[0]):
            for iw in range(0, disp.shape[1]):
                L2 += (disp[iv, iw]-disp1[iv, iw])**2
        # Send L2 values to master
        comm.send(L2, dest=0)

    # Block until all processes have reached this point.
    comm.Barrier()

    # Get L2 and fill particles history
    if rank == 0:
        # L2 results
        L2 = 0.
        for ip in range(1, 3):
            L2 += comm.recv(source=ip)
        L2 = np.sqrt(L2)
        # PSO update on master
        if(np.isnan(L2)):
            swarm.misfit[indv] = 1000.
        else:
            swarm.misfit[indv] = L2
        swarm.history[indv, :, :] = swarm.current[indv, :, :]
        #sys.stdout.write("\r%d%%" % int((indv+1)/(nindv)*100))
        #sys.stdout.flush()

# Block until all processes have reached this point.
comm.Barrier()

# PSO update
if rank == 0:
    swarm.update(control=1, topology='toroidal', ndim=3)
    print('*PSO first evaluation done\n', flush=True)


# ------------------------------------------------------------------
# >> Process
# ------------------------------------------------------------------

# Loop over generations
for igen in range(0, ngen):

    # Loop over particles
    for indv in range(0, nindv):

        # Coarse to fine grid
        if rank == 0:
            npts = swarm.pspace.shape[0]
            xp = swarm.current[indv, :, 0]
            zp = swarm.current[indv, :, 1]
            # S-wave velocity model
            val = swarm.current[indv, :, 2]
            vsmod = sibson2(npts, xp, zp, val, 51, 301, 0.5)
            # Density model
            val = swarm.current[indv, :, 3]
            romod = sibson2(npts, xp, zp, val, 51, 301, 0.5)
            # Poisson's ratio model
            val = swarm.current[indv, :, 4]
            numod = sibson2(npts, xp, zp, val, 51, 301, 0.5)
            # P-wave velocity model
            vpmod = vsnu2vp(vsmod, numod)

        # Broadcast velocity and density models to slaves.
        comm.Bcast([vpmod, MPI.FLOAT], root=0)
        comm.Bcast([vsmod, MPI.FLOAT], root=0)
        comm.Bcast([romod, MPI.FLOAT], root=0)

        # Calculate observed data and evaluate
        if rank != 0:
            # Seismic modeling
            dcalz = seismod(runpar, modpar, acqpar, vpmod, vsmod, romod)
            # Rayleigh dispersion
            disp1 = dcalz.masw(vmin=200., vmax=1200., dv=5., fmin=10., fmax=50.)
            disp1 /= np.amax(disp1)
            # L2-norm
            L2 = 0.
            for iv in range(0, disp.shape[0]):
                for iw in range(0, disp.shape[1]):
                    L2 += (disp[iv, iw]-disp1[iv, iw])**2
            # Send L2 values to master
            comm.send(L2, dest=0)

        # Block until all processes have reached this point.
        comm.Barrier()

        # Get L2 and fill particles history
        if rank == 0:
            # L2 results
            L2 = 0.
            for ip in range(1, 3):
                L2 += comm.recv(source=ip)
            L2 = np.sqrt(L2)
            # PSO update on master
            if L2 <= swarm.misfit[indv]:
                swarm.misfit[indv] = L2
                swarm.history[indv, :, :] = swarm.current[indv, :, :]

    # Block until all processes have reached this point.
    comm.Barrier()

    # PSO update
    if rank == 0:
        swarm.update(control=1, topology='toroidal', ndim=3)
        print('*PSO ', igen,
              np.amin(swarm.misfit[:]), np.mean(swarm.misfit[:]),
              '\n', flush=True)