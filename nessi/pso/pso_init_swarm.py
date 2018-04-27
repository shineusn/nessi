import numpy as np

def pso_init_swarm(nindv, pspace):

    # Get npts and npar from pspace
    npts = pspace.shape[0]
    npar = pspace.shape[1]

    # Create particle position and particle velocity vectors
    q = np.zeros((nindv, npts, npar), dtype=np.float32)
    v = np.zeros((nindv, npts, npar), dtype=np.float32)

    # Random generation of particle position
    for indv in range(0, nindv):
        for ipts in range(0, npts):
            for ipar in range(0,npar):
                r = np.random.random_sample()
                q[indv,ipts,ipar] = pspace[ipts,ipar,0] + \
                                    r*(pspace[ipts,ipar,1]-pspace[ipts,ipar,0])


    return q, v
