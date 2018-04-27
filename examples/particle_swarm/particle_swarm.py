import numpy as np

from nessi.pso import init_pspace
from nessi.pso import init_swarm

pspace = init_pspace('random_models.ascii')

print pspace.shape[0], pspace.shape[1], pspace.shape[2]

nindv = 49
q, v = init_swarm(nindv, pspace)

print q.shape[0], q.shape[1], q.shape[2]
