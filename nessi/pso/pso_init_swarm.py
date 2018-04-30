"""
Module pso_init_swarm
"""
import numpy as np

def pso_init_swarm(nindv, pspace):
    """
    Initialize all the particles of the swarm.
    """

    # Get npts and npar from pspace
    npts = pspace.shape[0]
    npar = pspace.shape[1]

    # Create particle position and particle velocity vectors
    p_current = np.zeros((nindv, npts, npar), dtype=np.float32)
    p_velocity = np.zeros((nindv, npts, npar), dtype=np.float32)

    # Random generation of particle position
    p_random = np.random.random_sample((npts, npar))
    for indv in range(0, nindv):
        p_current[indv, :, :] = pspace[:, :, 0]\
            +p_random*(pspace[:, :, 1]-pspace[:, :, 0])

    return p_current, p_velocity
