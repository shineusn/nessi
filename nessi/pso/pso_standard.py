import numpy as np

def pso_standard_update(q, v, ql, qg, pspace, \
                        c0=0.72, c1=2.05, c2=2.05, control=0, \
                        topology = 'full'):
    """
    update
    Standard PSO update using inertia weight or constriction factor approach.
    """

    # Get nindv, npts, npar from q shape
    nindv = q.shape[0]
    npts  = q.shape[1]
    npar  = q.shape[2]

    # Inertia weight (control=0 default)
    # Constriction factor (control=1)
    if(control == 0):
        cp = c1
        cg = c2
    elif(control == 1):
        cp = c0*c1
        cg = c0*c2

    # Update process
    for indv in range(0, nindv):
        for ipts in range(0, npts):
            for ipar in range(0, npar):
                
                # Trial
                r1 = np.radom.random_sample()
                r2 = np.random.random_sample()

                # Update velocity vector
                v[indv,ipts,ipar] = c0*v[indv,ipts,ipar]+ \
                                    cp*r1(ql[indv,ipts,ipar]-q[indv,ipts,ipar]) + \
                                    cg*r2(qg[indv,ipts,ipar]-q[indv,ipts,ipar])

                # Check particle velocity
                if(np.abs(v[indv][ipts][ipar])>pspace[ipts,ipar,2]):
                    v[indv,ipts,ipar] = np.sign(v[indv,ipts,ipar])*pspace[ipts,ipar,2]

                # Update particle position
                q[indv,ipts,ipar] += v[indv,ipts,ipar]

                # Check if particle is in parameter space
                if(q[indv,ipts,ipar] < pspace[ipts,ipar,0]):
                    q[indv,ipts,ipar] = pspace[ipts,ipar,0]
                if(q[indv,ipts,ipar] > pspace[ipts,ipar,1]):
                    q[indv,ipts,ipar] = pspace[ipts,ipar,1]
                
                
    return q, v
