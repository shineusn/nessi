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

import h5py

from nessi.io import SUdata
from nessi.globopt import Swarm
from nessi.modbuilder.interp2d import sibson2

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
# >> Initialize the swarm
# ------------------------------------------------------------------

# Initialize the number of generations and particles on master
# and slaves.
ngen = 0 # ngen is incremented at each new frequency band for layer stripping
nindv = 49

# Initialize the swarm on the master only.
if rank == 0:
    swarm = Swarm()
    swarm.init_pspace('input/random_models.ascii')

    # save original pspace
    pspace_save = swarm.pspace

# ------------------------------------------------------------------
# >> Layer-stripping approach
# ------------------------------------------------------------------

# Declare array of wavelenghts and frequencies
nstrip = 5
lbdtab = np.zeros(nstrip, dtype=np.float32)
frqtab = np.zeros(nstrip, dtype=np.float32)

# Fill tables
lbdtab[0] = 2.*6.13 ; frqtab[0] = 33.
lbdtab[1] = 2.*10.36; frqtab[1] = 24.
lbdtab[2] = 2.*16.43; frqtab[2] = 19.
lbdtab[3] = 2.*25.  ; frqtab[3] = 14.
lbdtab[4] = 2.*50.  ; frqtab[4] = 5.


# ------------------------------------------------------------------
# >> Process
# ------------------------------------------------------------------

# Initialize velocity and density models on slaves
if rank != 0:
    vpmod = np.zeros((51, 301), dtype=np.float32)
    vsmod = np.zeros((51, 301), dtype=np.float32)
    romod = np.zeros((51, 301), dtype=np.float32)
    
# >> Loop over max wavelenght (layer-stripping)
for istrip in range(0, nstrip):

    # Calculating the reference dispersion diagrams using the MASW method
    if rank != 0:
        disp, dvel, dfrq = dobsz.masw(vmin=200., vmax=1200., dv=5., fmin=frqtab[0], fmax=50.)
        disp /= np.amax(disp)
        print( len(disp), len(disp[0]))
               
    # Block until all processes have reached this point.
    comm.Barrier()

    # >> Initialize particles on master only
    if rank == 0:
        swarm.init_particles(nindv)
        
    # >> First evaluation
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
            disp1, dvel, dfrq = dcalz.masw(vmin=200., vmax=1200., dv=5., fmin=frqtab[istrip], fmax=50.)
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
            print('** 1st eval indv=', indv, ' misfit=', swarm.misfit[indv],'\n', flush=True)

    # Block until all processes have reached this point.
    comm.Barrier()

    # PSO update
    if rank == 0:
        swarm.update(control=1, topology='toroidal', ndim=7)
        print('*PSO first evaluation done\n', flush=True)
    
            
    # >> Loop over generations
    #    Increment negen for each new istrip
    ngen += 10
    for igen in range(0, ngen):
        
        # >> Evaluation
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
                disp1 = dcalz.masw(vmin=200., vmax=1200., dv=5., fmin=frqtab[istrip], fmax=50.)
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
                if(L2 < swarm.misfit[indv]):
                    swarm.misfit[indv] = L2
                    swarm.history[indv, :, :] = swarm.current[indv, :, :]
                print('** igen=', igen, ' indv=', indv, ' misfit=', swarm.misfit[indv],'\n', flush=True)
                
        # Block until all processes have reached this point.
        comm.Barrier()

        # PSO update
        if rank == 0:
            swarm.update(control=1, topology='toroidal', ndim=7)
            print('*PSO evaluation done. igen/istrip', igen, istrip, '\n', flush=True)

    # Fit
    if rank == 0:
        fit = np.zeros(nindv, dtype=np.float32)
        fit[:] = 1./swarm.misfit[:]
    
    # Last generation / Update parameter space
    if rank == 0:
        for ipts in range(0, npts):
            par = 0.
            if pspace_save[ipts, 1, 1] <= lbdtab[istrip]/2. :
                par = 0.
                for indv in range(0, nindv):
                    par += fit[indv]*swarm.history[indv, ipts, 2]
                par /= np.sum(fit)
                swarm.pspace[ipts, 2, 0] = 0.9*par
                swarm.pspace[ipts, 2, 1] = 1.1*par
                swarm.pspace[ipts, 2, 0] = 0.2*np.abs(1.1*par-0.9*par)
                if swarm.pspace[ipts, 2, 0] < pspace_save[ipts, 2, 0]:
                    swarm.pspace[ipts, 2, 0] = pspace_save[ipts, 2, 0]
                if swarm.pspace[ipts, 2, 1] > pspace_save[ipts, 2, 1]:
                    swarm.pspace[ipts, 2, 1] = pspace_save[ipts, 2, 1]
    
    # Save
    if rank == 0:
        h5file = h5py.File('swarm_'+str(istrip).zfill(2)+'_'+str(igen).zfill(3)+'.hdf5', 'a')
        group = h5file['/'+str(istrip).zfill(2)+'_'+str(igen).zfill(3)]
        # Save misfit
        datamisfit = group.create_dataset(name='misfit', data=swarm.misfit)
        # Save particle history
        for indv in range(0, nindv):
            dataparticle= group.create_dataset(name=str(indv).zfill(3),
                                               data=swarm.history[indv,:,:])
        h5file.flush()
        h5file.close()
