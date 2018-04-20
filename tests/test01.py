import numpy as np
import sys

sys.path.append('/home/pageotd/Work/nessi')
import lib as lib
from lib import pso

fmod = 'random_models.ascii'

pspace = pso.initpspace(fmod)

print pspace.shape[0], pspace.shape[1] 
