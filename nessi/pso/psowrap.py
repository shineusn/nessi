from numpy import loadtxt, zeros, float32
from ctypes import CDLL, c_int, c_float
from numpy.ctypeslib import ndpointer, load_library

class Swarm():

    def __init__(self):

        # Inertia weight/Constriction factor
        self.c0 = 0.
        
        # Congitive parameter
        self.c1 = 2.05

        # Social parameter
        self.c2 = 2.05

        # Inertia = 0 / Constriction = 1 
        self.constrict = 1

        # Number of points per particule
        self.npts = 0

        # Number of parameters per point
        self.npar = 0

        # PSO library
        self.clibpso = load_library('libpso',
                               '/home/pageotd/Work/nessi/nessi/pso/')
        
        # nessi_pso_bound
        self.clibpso.nessi_pso_bound.argtypes = [c_float, c_float]
        self.clibpso.nessi_pso_bound.restype = c_float

        # nessi_pso_init
        self.clibpso.nessi_pso_init.argtypes = [c_int, c_int, c_int,
                                                ndpointer(dtype=float32, ndim=3, flags='C_CONTIGUOUS'),
                                                ndpointer(dtype=float32, ndim=3, flags='C_CONTIGUOUS')]

        # nessi_pso_updt
        self.clibpso.nessi_pso_updt.argtypes = [c_int, c_int, c_int,
                                                ndpointer(dtype=float32, ndim=3, flags='C_CONTIGUOUS'),
                                                ndpointer(dtype=float32, ndim=2, flags='C_CONTIGUOUS'),
                                                ndpointer(dtype=float32, ndim=3, flags='C_CONTIGUOUS'),
                                                c_float, c_float, c_float, c_int,
                                                ndpointer(dtype=float32, ndim=3, flags='C_CONTIGUOUS'),
                                                ndpointer(dtype=float32, ndim=3, flags='C_CONTIGUOUS')]
        
    def initpspace(self, fmod):
        """
        initpspace
        Create a table containing the parameter space boundaries.
        """

        # Load pspace file in a temporary array
        tmp = loadtxt(fmod, comments='#')

        # Check the number of points per particule
        try:
            self.npts = int(len(tmp))
            self.npar = int(len(tmp[0])/3)
        except:
            self.npts = 1
            self.npar = int(len(tmp)/2)

        # Initialize pspace array
        self.pspace = zeros((self.npts, self.npar, 3), dtype=float32)

        # Fill pspace array
        for ipts in range(0, self.npts):
            i = 0
            if(self.npts == 1):
                for ipar in range(0, self.npar):
                    self.pspace[ipts, ipar, 0] = tmp[i]
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
        """
        initswarm
        Initialize all particles and their related vectors.
        """
        
        # Initilize the swarm (current particles)
        self.current = zeros((self.nindv, self.npts, self.npar), dtype=float32, order='C')

        # Initialize particles velocity
        self.velocity = zeros((self.nindv, self.npts, self.npar), dtype=float32, order='C')
        
        # Initialize particles history (pbest)
        self.pbest = zeros((self.nindv, self.npts, self.npar), dtype=float32, order='C')

        # Initialize swarm global best particle (gbest)
        self.gbest = zeros((self.npts, self.npar), dtype=float32, order='C')

        # Initialize particles misfit/fit
        self.misfit = zeros((self.nindv), dtype=float32, order='C')
        
        # Initialize first generation of particles
        self.clibpso.nessi_pso_init(self.nindv, self.npts, self.npar,
                                    self.pspace, self.current)
    
        return

    def update(self):
        """
        update
        Standard PSO update using inertia weight or constriction factor approach.
        """
        self.clibpso.nessi_pso_updt(self.nindv, self.npts, self.npar,
                                    self.pbest, self.gbest, self.pspace,
                                    self.c0, self.c1, self.c2, self.constrict,
                                    self.current, self.velocity)
        return
