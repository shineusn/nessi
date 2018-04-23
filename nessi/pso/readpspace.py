from numpy import loadtxt, zeros, float32

def readpspace(fmod):
    """
    readpspace
    Create table containing search space boundaries for each parameter.
    """
    tmp = loadtxt(fmod, comments='#')
    try:
        npts = int(len(tmp))
        npar = int(len(tmp[0])/3)
    except:
        npts = 1
        npar = int(len(tmp)/2)
    pspace = zeros((npts, npar, 3), dtype=float32)
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
