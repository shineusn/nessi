import numpy as np
from numpy import loadtxt, zeros, float32

def pso_init_pspace(fmod):
    """
    initpspace
    Create a table containing the parameter space boundaries.
    """
    
    # Load pspace file in a temporary array
    tmp = loadtxt(fmod, comments='#')
    
    # Check the number of points per particule
    try:
        npts = int(len(tmp))
        npar = int(len(tmp[0])/3)
    except:
        npts = 1
        npar = int(len(tmp)/2)
        
    # Initialize pspace array
    pspace = zeros((npts, npar, 3), dtype=float32)
    
    # Fill pspace array
    for ipts in range(0, npts):
        i = 0
        if(npts == 1):
            for ipar in range(0, npar):
                pspace[ipts, ipar, 0] = tmp[i]
                pspace[ipts, ipar, 1] = tmp[i+1]
                pspace[ipts, ipar, 2] = tmp[i+2]
                i += 3
        else:       
            for ipar in range(0, npar):
                pspace[ipts, ipar, 0] = tmp[ipts, i]
                pspace[ipts, ipar, 1] = tmp[ipts, i+1]
                pspace[ipts, ipar, 2] = tmp[ipts, i+2]
                i += 3
                    
    return pspace
