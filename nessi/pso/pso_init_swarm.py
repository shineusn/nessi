"""
Module pso_init_swarm
"""
import numpy as np


def pso_init_swarm(particles, pspace):
    """
    Initialize all the particles of the swarm.
    """

    # Get nindv, npts and npar from particles and pspace
    nindv = len(particles)
    npts = pspace.shape[0]
    npar = pspace.shape[1]

    # Random generation of particle position
    p_random = np.random.random_sample((npts, npar))
    for indv in range(0, nindv):
        particles[indv]['current'][:, :] = pspace[:, :, 0]\
                                    + p_random*(pspace[:, :, 1]-pspace[:, :, 0])

    return
