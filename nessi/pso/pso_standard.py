"""
Module pso_standard_update
"""
import numpy as np

def pso_standard_update(q_c, v_c, q_l, q_g, pspace, \
                        c_0=0.72, c_1=2.05, c_2=2.05, control=0, \
                        topology='full'):
    """
    update
    Standard PSO update using inertia weight or constriction factor approach.
    """

    # Inertia weight (control=0 default)
    # Constriction factor (control=1)
    if control == 0:
        c_p = c_1
        c_g = c_2
    elif control == 1:
        c_p = c_0*c_1
        c_g = c_0*c_2

    # Update process
    for indv in range(0, q_c.shape[0]):
        for ipts in range(0, q_c.shape[1]):
            for ipar in range(0, q_c.shape[2]):

                # Update velocity vector
                v_c[indv, ipts, ipar] = c_0*v_c[indv, ipts, ipar]\
                                        +c_p*np.random.random_sample()\
                                        *(q_l[indv, ipts, ipar]-q_c[indv, ipts, ipar])\
                                        +c_g*np.random.random_sample()\
                                        *(q_g[indv, ipts, ipar]-q_c[indv, ipts, ipar])

                # Check particle velocity
                if(np.abs(v_c[indv, ipts, ipar]) > pspace[ipts, ipar, 2]):
                    v_c[indv, ipts, ipar] = np.sign(v_c[indv, ipts, ipar])\
                                            *pspace[ipts, ipar, 2]

                # Update particle position
                q_c[indv, ipts, ipar] += v_c[indv, ipts, ipar]

                # Check if particle is in parameter space
                if(q_c[indv, ipts, ipar] < pspace[ipts, ipar, 0]):
                    q_c[indv, ipts, ipar] = pspace[ipts, ipar, 0]
                if(q_c[indv, ipts, ipar] > pspace[ipts, ipar, 1]):
                    q_c[indv, ipts, ipar] = pspace[ipts, ipar, 1]

    return q_c, v_c
