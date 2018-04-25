import numpy as np
import sys
import matplotlib.pyplot as plt
from nessi.pso import Swarm
from nessi.grd import voronoi, idweight, sibson1, sibson2

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

n1 = 51
n2 = 301
dh = 0.5

vs1 = voronoi(q.npts,
             q.current[0,:,0], q.current[0,:,1],
             q.current[0,:,2],
             n1, n2, dh)

pw = 2
vs2 = idweight(q.npts,
              q.current[0,:,0], q.current[0,:,1],
              q.current[0,:,2],
              pw, n1, n2, dh)

vs3 = sibson1(q.npts,
              q.current[0,:,0], q.current[0,:,1],
              q.current[0,:,2],
              n1, n2, dh)

vs4 = sibson2(q.npts,
              q.current[0,:,0], q.current[0,:,1],
              q.current[0,:,2],
              n1, n2, dh)

plt.subplot(411)
plt.imshow(vs1, aspect='auto', cmap='jet')
plt.subplot(412)
plt.imshow(vs2, aspect='auto', cmap='jet')
plt.subplot(413)
plt.imshow(vs3, aspect='auto', cmap='jet')
plt.subplot(414)
plt.imshow(vs4, aspect='auto', cmap='jet')
plt.show() 
