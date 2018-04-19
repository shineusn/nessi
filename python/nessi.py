from numpy.ctypeslib import load_library, ndpointer
from numpy import float32
from numpy import zeros
from numpy import loadtxt
from ctypes import c_int, c_float, c_double
from os import getcwd

pwd = getcwd()


# ------------------------------------------------------------
# >> LOAD C LIBRARIES
# ------------------------------------------------------------
#lpso = load_library('libpso', '/home/pageotd/Work/PROSE/nessi/lib/') 
lgrd = load_library('libgrd', '/home/pageotd/Work/PROSE/nessi/lib/') 
ldsp = load_library('libdsp', '/home/pageotd/Work/PROSE/nessi/lib/')

class pso():

    def __init__(self):
        # >> LOAD C SHARED LIBRARY
        self.lpso = load_library('libpso', '/home/pageotd/Work/PROSE/nessi/lib/')
        return
    
    def parspace(self, fpspace):
        """
        parspace
        Create table containing search space boundaries for each parameter.
        """
        # >> Load from file
        tmp = loadtxt(fpspace, comments='#')
        # >> Check dimensions
        try:
            self.npts = int(len(tmp))
            self.npar = int(len(tmp[0])/3)
        except:
            self.npts = 1
            self.npar = int(len(tmp)/2)
        # >> Declare parameter space array 
        self.pspace = zeros((self.npts, self.npar, 3), dtype=float32, order='C')
        # >> Fill parameter space array
        for ipts in range(0, self.npts):
            i = 0
            if(self.npts == 1):
                for ipar in range(0, self.npar):
                    self.psapce[ipts, ipar, 0] = tmp[i]
                    self.pspace[ipts, ipar, 1] = tmp[i+1]
                    self.pspace[ipts, ipar, 2] = tmp[i+2]
                    i += 3
            else:       
                for ipar in range(0, self.npar):
                    self.pspace[ipts, ipar, 0] = tmp[ipts, i]
                    self.pspace[ipts, ipar, 1] = tmp[ipts, i+1]
                    self.pspace[ipts, ipar, 2] = tmp[ipts, i+2]
                    i += 3
                
        return 


    def initswarm(self):
        # >> Declare population array
        self.q = zeros((self.nindv, self.npts, self.npar), dtype=float32, order='C')
        # >> Declare 3D array of floats
        arr3df = ndpointer(dtype=float32, ndim=3, flags='C_CONTIGUOUS')
        # >> Declare C-function's arguments
        self.lpso.nessi_pso_init.argtypes = [c_int, c_int, c_int, arr3df, arr3df]
        # >> Call C-function
        self.lpso.nessi_pso_init(self.nindv, self.npts, self.npar, self.pspace, self.q)
        return
