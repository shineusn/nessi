from numpy import zeros, loadtxt
from numpy import float32

def initpspace(fpspace):
    """
    initpspace
    Read the file containing the parameter space
    boundaries and Vmax for each parameter of each point.
    """

    # Load the parameter space file in tmp array
    tmp = loadtxt(fpspace)

    # Check number of points
    try:
        npts = int(len(tmp))
        npar = int(len(tmp[0])/3)
    except:
        npts = 1
        npar = int(len(tmp)/3)

    # Declare pspace array
    pspace = zeros((npts, npar, 3), dtype=float32, order='C')

    # Fill pspace array
    for ipts in range(0, npts):
        i = 0
        for ipar in range(0, npar):
            if(npts == 1):
                pspace[ipts,ipar,0] = tmp[i]
                pspace[ipts,ipar,1] = tmp[i+1]
                pspace[ipts,ipar,2] = tmp[i+2]
            else:
                pspace[ipts,ipar,0] = tmp[ipts,i]
                pspace[ipts,ipar,1] = tmp[ipts,i+1]
                pspace[ipts,ipar,2] = tmp[ipts,i+2]
            i += 3

    return pspace
