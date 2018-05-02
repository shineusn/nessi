"""
Module pso_update is a collection of functions which allows to update
the swarm using an update formula (standard, fully-informed) and a
topology (full, ring1, ring2, van Neumann, Moore).
"""
import numpy as np


def _pso_parser(kwargs):
    """
    Parse the kwarg parameter list of pso_standard_update function
    and calculate control parameter values.
    """

    control = kwargs.get('control', 0)

    cpar = np.zeros(3, dtype=np.float32)
    cpar[0] = kwargs.get('c_0', 0.72)

    if control == 0:
        # Inertia weight (control=0 default)
        cpar[1] = kwargs.get('c_1', 2.05)
        cpar[2] = kwargs.get('c_2', 2.05)
    else:
        # Constriction factor (control=1)
        cpar[1] = kwargs.get('c_1', 2.05)\
                  * kwargs.get('c_0', 0.7298)
        cpar[2] = kwargs.get('c_2', 2.05)\
                  * kwargs.get('c_1', 0.72)

    topology = kwargs.get('topology', 'full')

    return cpar, topology

def get_gbest(particles, topology, indv=0, ndim=0):
    """
    Get gbest particle of the whole swarm or in the neighborhood of
    a given particle.
    """

    # Get the best particle of the whole swarm
    if topology == 'full':
        ibest = np.argmin(particles[:]['misfit'])
        gbest = particles[ibest]['history']

    # Get the particle in the neighborhood (1 left, 1 right)
    #of the particle including itself.
    if topology == 'ring1':
        ibest = np.argmin(particles[indv-1:indv+1]['misfit'])
        gbest = particles[ibest]['history']

    # Get the particle in the neighborhood (2 left, 2 right)
    #of the particle including itself.
    if topology == 'ring2':
        ibest = np.argmin(particles[indv-2:indv+2]['misfit'])
        gbest = particles[ibest]['history']

    return gbest

def pso_standard_update(particles, pspace, **kwargs):
    """
    Standard PSO update.
    """

    # Parse kwargs parameter list
    cpar, topology = _pso_parser(kwargs)

    # Update process
    for indv in range(0, particles.shape[0]):
        gbest = get_gbest(particles, topology, indv)
        for ipts in range(0, pspace.shape[0]):
            for ipar in range(0, pspace.shape[1]):

                # Get values
                velocity = particles[indv]['velocity'][ipts, ipar]
                history = particles[indv]['history'][ipts, ipar]
                current = particles[indv]['current'][ipts, ipar]

                # Update velocity vector
                particles[indv]['velocity'][ipts, ipar] = cpar[0]*velocity\
                                        + cpar[1]*np.random.random_sample()\
                                        * (history-current)\
                                        + cpar[2]*np.random.random_sample()\
                                        * (gbest[ipts,ipar]-current)

                # Check particle velocity
                # vvv = particles[ibest]['history'][ipts,ipar]
                if(np.abs(particles[indv]['history'][ipts, ipar]) > pspace[ipts, ipar, 2]):
                    particles[indv]['velocity'][ipts, ipar] = \
                        np.sign(particles[indv]['velocity'][ipts, ipar])\
                        * pspace[ipts, ipar, 2]

                # Update particle position
                particles[indv]['current'][ipts, ipar] += particles[indv]['velocity'][ipts, ipar]

                # Check if particle is in parameter space
                if(particles[indv]['current'][ipts, ipar] < pspace[ipts, ipar, 0]):
                    particles[indv]['current'][ipts, ipar] = pspace[ipts, ipar, 0]
                if(particles[indv]['current'][ipts, ipar] > pspace[ipts, ipar, 1]):
                    particles[indv]['current'][ipts, ipar] = pspace[ipts, ipar, 1]
    return