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

# Import modules
import h5py
import gprMax
import sys
import numpy as np
import matplotlib.pyplot as plt
from nessi.globopt import Swarm
import os

# CREATE GPRMAX INPUT
def create_gprmax_input(x, y, r):
    """
    Create a simple input copy from Bscan example where
    only the cylinder is edited
    """
    gprinput = open('gprmax_input.in', 'w')

    # title
    gprinput.write('#title: B-scan from a metal cylinder buried in a dielectric half-space\n')
    # domain
    gprinput.write('#domain: 0.240 0.210 0.002\n')
    # dx dy dz
    gprinput.write('#dx_dy_dz: 0.002 0.002 0.002\n')
    # time window
    gprinput.write('#time_window: 3e-9\n\n')
    # materials
    gprinput.write('#material: 6 0 1 0 half_space\n\n')
    # waveform
    gprinput.write('#waveform: ricker 1 1.5e9 my_ricker\n')
    # hertzian dipole
    gprinput.write('#hertzian_dipole: z 0.040 0.170 0 my_ricker\n')
    # rx
    gprinput.write('#rx: 0.080 0.170 0\n')
    # src step
    gprinput.write('#src_steps: 0.010 0 0\n')
    # rx step
    gprinput.write('#rx_steps: 0.010 0 0\n\n')
    # box
    gprinput.write('#box: 0 0 0 0.240 0.170 0.002 half_space\n')
    # cylinder
    gprinput.write('#cylinder: '+str(x)+' '+str(y)+' 0 '+str(x)+' '+str(y)+' 0.002 '+str(r)+' pec\n')

    gprinput.close()

# RUN GPRMAX
def gprmax_modeling():
    """
    Run gprMax and return needed calculated data
    """
    # No terminal output
    #sys.stdout = open('file', 'w')

    # Run gprMax
    n = 11
    run_name = 'gprmax_input'
    gprMax.run(run_name+'.in', n=n)

    # Read outputs
    for i in range(0,n):
        gprout = h5py.File(run_name+str(i+1)+'.out', 'r')
        if i == 0:
            tmp = gprout.get('/rxs/rx1/Ez')
            ns = len(np.array(tmp))
            # Declare array
            Ez = np.zeros((ns, n), dtype=np.float32)
            Hx = np.zeros((ns, n), dtype=np.float32)
            Hy = np.zeros((ns, n), dtype=np.float32)
        Ez[:,i] = np.array(gprout.get('/rxs/rx1/Ez'))
        Hx[:,i] = np.array(gprout.get('/rxs/rx1/Hx'))
        Hy[:,i] = np.array(gprout.get('/rxs/rx1/Hy'))

    #sys.stdout.close()

    return Ez, Hx, Hy


# Observed data
xobs = 0.120
yobs = 0.080
robs = 0.010

create_gprmax_input(xobs, yobs, robs)
Ezobs, Hxobs, Hyobs = gprmax_modeling()

plt.subplot(131)
plt.imshow(Ezobs, aspect='auto', cmap='gray')
plt.subplot(132)
plt.imshow(Hxobs, aspect='auto', cmap='gray')
plt.subplot(133)
plt.imshow(Hyobs, aspect='auto', cmap='gray')
plt.show()


# ------------------------------------------------------------------
# >> Initialize the swarm
# ------------------------------------------------------------------

# Initialize the number of generations and particles
ngen = 50
nindv = 16
ndim = 4

# Initialize the swarm
swarm = Swarm()
swarm.init_pspace('input/random_model.ascii')
swarm.init_particles(nindv)

# ------------------------------------------------------------------
# >> First evaluation
# ------------------------------------------------------------------

# Loop over individuals
for indv in range(0, nindv):
    print(indv)
    # Forward modeling
    xq = swarm.current[indv, 0, 0]
    yq = swarm.current[indv, 0, 1]
    rq = swarm.current[indv, 0, 2]
    create_gprmax_input(xq, yq, rq)
    Ezcal, Hxcal, Hycal = gprmax_modeling()
    # Misfit
    L2 = 0.
    for j in range(0, len(Ezcal[0])):
        for i in range(0, len(Ezcal)):
            L2 += (Ezobs[i,j]-Ezcal[i,j])**2+(Hxobs[i,j]-Hxcal[i,j])**2+(Hyobs[i,j]-Hycal[i,j])**2
    L2 = np.sqrt(L2)
    swarm.misfit[indv] = L2
    swarm.history[indv, :, :] = swarm.current[indv, :, :]

# ------------------------------------------------------------------
# >> Process
# ------------------------------------------------------------------

fgpr = open('gpr_pso.txt', 'w')
for igen in range(0, ngen):
    fgpr.write('gen='+str(igen)+' misfit='+str(np.mean(swarm.misfit[:]))+' best='+str(np.amin(swarm.misfit[:]))+'\n')
    print('\n\n gen=',igen, ' misfit=', np.mean(swarm.misfit[:]), ' best=', np.amin(swarm.misfit[:]), '\n\n')

    # Update the Swarm
    swarm.update(control=1, topology='toroidal', ndim=ndim)

    # Evaluation
    for indv in range(0, nindv):
        print(indv)
        # Forward modeling
        xq = swarm.current[indv, 0, 0]
        yq = swarm.current[indv, 0, 1]
        rq = swarm.current[indv, 0, 2]
        create_gprmax_input(xq, yq, rq)
        Ezcal, Hxcal, Hycal = gprmax_modeling()
        # Misfit
        L2 = 0.
        L2Ez_num = 0.
        L2Ez_den = 0.
        L2Hx_num = 0.
        L2Hx_den = 0.
        L2Hy_num = 0.
        L2Hy_den = 0.
        
        for j in range(0, len(Ezcal[0])):
            for i in range(0, len(Ezcal)):
                L2 += (Ezobs[i,j]-Ezcal[i,j])**2+(Hxobs[i,j]-Hxcal[i,j])**2+(Hyobs[i,j]-Hycal[i,j])**2
        L2 = np.sqrt(L2)
        # Test
        if L2 < swarm.misfit[indv]:
            swarm.misfit[indv] = L2
            swarm.history[indv, :, :] = swarm.current[indv, :, :]
            
    fgen = open('fgen'+str(igen).zfill(3)+'.txt', 'w')
    for indv in range(0, nindv):
        fgen.write(str(swarm.misfit[indv])+' ')
        fgen.write(str(swarm.history[indv, 0, 0])+' ')
        fgen.write(str(swarm.history[indv, 0, 1])+' ')
        fgen.write(str(swarm.history[indv, 0, 2])+' ')
        fgen.write('\n')
        
    fgen.close()
# Get best
ibest = np.argmin(swarm.misfit[:])
print(swarm.history[ibest,:,:])
