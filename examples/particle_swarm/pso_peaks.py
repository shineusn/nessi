#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: pso_peaks.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
PSO example using the 2D peaks function.
:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

import numpy as np
import matplotlib.pyplot as plt

from nessi.pso import init_pspace
from nessi.pso import init_swarm
from nessi.pso import particles
from nessi.pso import standard_update

def peaksF(x1min, x1max, dx1, x2min, x2max, dx2):
    """
    Return an array containing the 2D Rastrigin function.
    """

    # >> Determine the number of samples
    n1 = int((x1max-x1min)/dx1)+1
    n2 = int((x2max-x2min)/dx2)+1

    # >> Declare array
    f = np.zeros((n1, n2), dtype=np.float32)

    # >> Fill the array
    for i2 in range(0, n2):
        x2 = x2min+float(i2)*dx2
        for i1 in range(0, n1):
            x1 = x1min+float(i1)*dx1
            f[i1, i2] = 3.*(1.-x1)*(1.-x1)\
                        *np.exp(-1.*x1*x1-(x2+1.)*(x2+1.))\
                        -10.*(x1/5.-x1*x1*x1-x2*x2*x2*x2*x2)\
                        *np.exp(-1.*x1*x1-x2*x2)\
                        -1./3.*np.exp(-1.*(x1+1)*(x1+1)-x2*x2)

    return f

def peaksEval(x1, x2):
    """
    Calculate the value of the 2D Rastrigin function at
    position (x1, x2).

    Input:
     - x1: position along axis 1
     - x2: position along axis 2

    Return:
     - value of 2D Rastrigin function
    """

    f = 3.*(1.-x1)*(1.-x1)\
        *np.exp(-1.*x1*x1-(x2+1.)*(x2+1.))\
        -10.*(x1/5.-x1*x1*x1-x2*x2*x2*x2*x2)\
        *np.exp(-1.*x1*x1-x2*x2)\
        -1./3.*np.exp(-1.*(x1+1)*(x1+1)-x2*x2)

    return f

fmod = 'pspace_peaks.ascii'
pspace = init_pspace(fmod)

ngen = 500
nindv = 10
swarm = particles(nindv, pspace.shape[0], pspace.shape[1])

fit = np.zeros((ngen+1, 2), dtype=np.float32)

# Initialize the swarm
init_swarm(swarm, pspace)

# First evaluation
for indv in range(0, nindv):
    swarm[indv]['misfit'] = \
        peaksEval(swarm[indv]['current'][0, 0], swarm[indv]['current'][0, 1])
fit[0, 0] = np.amax(swarm[:]['misfit'])
fit[0, 1] = np.mean(swarm[:]['misfit'])

# Loop over generations
for igen in range(0, ngen):
    # Update the swarm
    standard_update(swarm, pspace, control=1)
    # Evaluation
    for indv in range(0, nindv):
        fit_value = peaksEval(swarm[indv]['current'][0, 0], swarm[indv]['current'][0, 1])
        if fit_value > swarm[indv]['misfit']:
            swarm[indv]['misfit'] = fit_value
            swarm[indv]['history'] = swarm[indv]['current']
    print(igen, np.amax(swarm[:]['misfit']), np.mean(swarm[:]['misfit']))
    fit[igen+1, 0] = np.amax(swarm[:]['misfit'])
    fit[igen+1, 1] = np.mean(swarm[:]['misfit'])

F = peaksF(-3.0, 3.0, 0.1, -3.0, 3.0, 0.1)
plt.subplot(121)
plt.xlim(-3.0, 3.0)
plt.ylim(-3.0, 3.0)
plt.imshow(F, aspect='auto', cmap='jet', extent=[-3.0, 3.0, -3.0, 3.0])
for indv in range(0, nindv):
    plt.scatter(swarm[indv]['history'][0, 1], swarm[indv]['history'][0, 0],
                color='black')
plt.subplot(122)
plt.plot(fit[:, 0], color='red')
plt.plot(fit[:, 1], color='gray')
plt.show()
