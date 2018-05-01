"""
Module pso_standard_update
"""
import numpy as np


def _pso_parser(kwargs):
    """
    Parser
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
                  * kwargs.get('c_0', 0.72)
        cpar[2] = kwargs.get('c_2', 2.05)\
                  * kwargs.get('c_1', 0.72)
        
    topology = kwargs.get('topology', 'full')

    return cpar, topology


def pso_standard_update(q_c, v_c, q_l, q_g, pspace, **kwargs):
    """
    update
    Standard PSO update using inertia weight or constriction factor approach.
    """

    cpar, control, topology = _pso_parser(kwargs)

    # Update process
    for indv in range(0, q_c.shape[0]):
        for ipts in range(0, q_c.shape[1]):
            for ipar in range(0, q_c.shape[2]):

                # Update velocity vector
                v_c[indv, ipts, ipar] = c_0*v_c[indv, ipts, ipar]\
                                        + c_p*np.random.random_sample()\
                                        * (q_l[indv, ipts, ipar]
                                           - q_c[indv, ipts, ipar])\
                                        + c_g*np.random.random_sample()\
                                        * (q_g[ipts, ipar]
                                           - q_c[indv, ipts, ipar])

                # Check particle velocity
                if(np.abs(v_c[indv, ipts, ipar]) > pspace[ipts, ipar, 2]):
                    v_c[indv, ipts, ipar] = np.sign(v_c[indv, ipts, ipar])\
                                            * pspace[ipts, ipar, 2]

                # Update particle position
                q_c[indv, ipts, ipar] += v_c[indv, ipts, ipar]

                # Check if particle is in parameter space
                if(q_c[indv, ipts, ipar] < pspace[ipts, ipar, 0]):
                    q_c[indv, ipts, ipar] = pspace[ipts, ipar, 0]
                if(q_c[indv, ipts, ipar] > pspace[ipts, ipar, 1]):
                    q_c[indv, ipts, ipar] = pspace[ipts, ipar, 1]

    return q_c, v_c
