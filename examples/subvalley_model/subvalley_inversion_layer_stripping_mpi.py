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
from cymasw import cmasw

from seismod import seismod

def vsnu2vp(vsmod, numod):
    vpmod = np.sqrt(vsmod*vsmod*2.*(1.-numod)/(1.-2.*numod))
    return vpmod

def dmasw(dataz, vmin=200., vmax=1200., dv=5., fmin=5., fmax=50.):
    scalco = dataz.header[0]['scalco']
    if scalco < 0:
        scale = -1./float(scalco)
    if scalco == 0:
        scale= 1.
    if scalco > 0:
        scale = float(scalco)
    scalel = dataz.header[0]['scalel']
    if scalel < 0:
        scalelev = -1./float(scalel)
    if scalel == 0:
        scalelev= 1.
    if scalel > 0:
        scalelev = float(scalel)
        
    dt = dataz.header[0]['dt']/1000000.
    sx = np.float32(dataz.header[0]['sx']*scale)
    sy = np.float32(dataz.header[0]['sy']*scale)
    sz = np.float32(dataz.header[0]['selev']*scalelev)
    nr = len(dataz.trace)
    gx = np.zeros(nr, dtype=np.float32)
    gy = np.zeros(nr, dtype=np.float32)
    gz = np.zeros(nr, dtype=np.float32)
    for ir in range(0, nr):
        gx[ir] = dataz.header[ir]['gx']*scale
        gy[ir] = dataz.header[ir]['gy']*scale
        gz[ir] = dataz.header[ir]['gelev']*scalelev
    disp, vel, frq = cmasw(dataz.trace, dt, sx, sz, gx, gz, vmin=vmin, vmax=vmax, dv=dv, fmin=fmin, fmax=fmax)
    
    return disp, vel, frq

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
    scalel = dobsz.header[0]['scalel']
    if scalel < 0:
        scalelev = -1./float(scalel)
    else:
        scalelev = float(scalel)
        
    # Get the source position
    sx = dobsz.header[0]['sx']*scale
    sz = dobsz.header[0]['selev']*scalelev

    # Get the receiver line
    nrec = len(dobsz.header)
    acq = np.zeros((nrec, 2), dtype=np.float32)
    for ir in range(0, nrec):
        acq[ir, 0] = dobsz.header[ir]['gx']*scale
        acq[ir, 1] = dobsz.header[ir]['gelev']*scalelev


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
nindv = 30

# Initialize the swarm on the master only.
if rank == 0:
    swarm = Swarm()
    swarm.init_pspace('input/pspace.ascii')

    # save original pspace
    pspace_save = np.zeros(np.shape(swarm.pspace), dtype=np.float32)
    pspace_save[:, :, :] = swarm.pspace[:, :, :]

# ------------------------------------------------------------------
# >> Layer-stripping approach
# ------------------------------------------------------------------

# Declare array of wavelenghts and frequencies
nstrip = 4
lbdtab = np.zeros(nstrip, dtype=np.float32)
frqtab = np.zeros(nstrip, dtype=np.float32)

# Fill tables
lbdtab[0] = 2.*8.00; frqtab[0] = 27.
lbdtab[1] = 2.*15  ; frqtab[1] = 20.
lbdtab[2] = 2.*25. ; frqtab[2] = 14.
lbdtab[3] = 2.*50. ; frqtab[3] = 10.

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
        disp, dvel, dfrq = dmasw(dobsz, vmin=200., vmax=1200., dv=5., fmin=frqtab[istrip], fmax=50.)
        disp /= np.amax(disp)
               
    # Block until all processes have reached this point.
    comm.Barrier()

    # >> Initialize particles on master only
    if rank == 0:
        swarm.init_particles(nindv, ncvt=500)
        
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

        # Calculate data and evaluate
        if rank != 0:
            # Seismic modeling
            dcalz = seismod(runpar, modpar, acqpar, vpmod, vsmod, romod)
            # Rayleigh dispersion
            disp1, dvel1, dfrq1 = dmasw(dcalz, vmin=200., vmax=1200., dv=5., fmin=frqtab[istrip], fmax=50.)
            disp1 /= np.amax(disp1)
            # L2-norm
            L2 = 0.
            LH = 0.
            A = (disp[:, :]-disp1[:, :]).flatten()
            L2 = np.sum(np.dot(A.T, A))
            #for iv in range(0, disp.shape[0]):
            #    for iw in range(0, disp.shape[1]):
            #        L2 += (disp[iv, iw]-disp1[iv, iw])**2
            # Send L2 values to master
            comm.send(L2, dest=0)

        # Block until all processes have reached this point.
        comm.Barrier()
    
        # Get L2 and fill particles history
        if rank == 0:
            # L2 results
            L2 = 0.
            for ip in range(1, 4):
                L2 += comm.recv(source=ip)
            L2 = np.sqrt(L2)
            # PSO update on master
            if(np.isnan(L2)):
                swarm.misfit[indv] = 10000000.
            else:
                swarm.misfit[indv] = L2
            swarm.history[indv, :, :] = swarm.current[indv, :, :]
            print('** 1st eval indv=', indv, ' misfit=', swarm.misfit[indv],'\n', flush=True)

    # Block until all processes have reached this point.
    comm.Barrier()

    # PSO update
    if rank == 0:
        swarm.update(control=1, topology='toroidal', ndim=5)
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
                disp1, dvel1, dfrq1 = dmasw(dcalz, vmin=200., vmax=1200., dv=5., fmin=frqtab[istrip], fmax=50.)
                disp1 /= np.amax(disp1)
                # L2-norm
                L2 = 0.
                LH = 0.
                A = (disp[:, :]-disp1[:, :]).flatten()
                L2 = np.sum(np.dot(A.T, A))
                #for iv in range(0, disp.shape[0]):
                #    for iw in range(0, disp.shape[1]):
                #        L2 += (disp[iv, iw]-disp1[iv, iw])**2
                # Send L2 values to master
                comm.send(L2, dest=0)
                
            # Block until all processes have reached this point.
            comm.Barrier()

            # Get L2 and fill particles history
            if rank == 0:
                # L2 results
                L2 = 0.
                for ip in range(1, 4):
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
            swarm.update(control=1, topology='toroidal', ndim=5)
            print('*PSO evaluation done. igen/istrip', igen, istrip, '\n', flush=True)

        # Fit
        if rank == 0:
            fit = np.zeros(nindv, dtype=np.float32)
            fit[:] = 1./swarm.misfit[:]

        # Save
        if rank == 0:
            h5file = h5py.File('swarm_'+str(istrip).zfill(2)+'_'+str(igen).zfill(3)+'.hdf5', 'w')
            group = h5file.create_group('/'+str(istrip).zfill(2)+'_'+str(igen).zfill(3))
            # Save misfit
            datamisfit = group.create_dataset(name='misfit', data=swarm.misfit)
            # Save particle history
            for indv in range(0, nindv):
                dataparticle= group.create_dataset(name=str(indv).zfill(3),
                                               data=swarm.history[indv,:,:])
            h5file.flush()
            h5file.close()

    if rank == 0:
        npts = swarm.pspace.shape[0]
        npar = swarm.pspace.shape[1]
        for ipts in range(0, npts):
            if pspace_save[ipts, 1, 1] <= lbdtab[istrip]/2. :
                swarm.pspace[ipts, 2, 0] = np.mean(swarm.history[:, ipts, 2])-np.std(swarm.history[:, ipts, 2])
                swarm.pspace[ipts, 2, 1] = np.mean(swarm.history[:, ipts, 2])+np.std(swarm.history[:, ipts, 2])
                swarm.pspace[ipts, 2, 2] = 0.2*np.abs(swarm.pspace[ipts, 2, 1]-swarm.pspace[ipts, 2, 0])
        print(swarm.pspace, flush=True)
