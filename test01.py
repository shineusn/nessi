import numpy as np
import sys
from nessi.pso import Swarm

fmod = 'random_models.ascii'

# Initialize particle swarm optimization
q = Swarm()

# Give the number of individuals
q.nindv = 1

# Initialize parameter space
q.initpspace(fmod)
print q.npts, q.npar

# Initialize the swarm with randomly generated particles
q.initswarm()
