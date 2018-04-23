import numpy as np
import sys
import nessi.pso

fmod = 'random_models.ascii'

pspace = nessi.pso.readpspace(fmod)

print pspace.shape[0], pspace.shape[1] 
