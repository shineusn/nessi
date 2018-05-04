import numpy as np
import matplotlib.pyplot as plt
import copy

from nessi.io import SUdata


musc = SUdata()

musc.read('musc_F50_01.su')
#plt.subplot(121)
#musc.image()

muscw = copy.deepcopy(musc)
#print(musc.header[0]['ns'].flags)
muscw.wind(tmin=-0.0, tmax=0.3)
#plt.subplot(122)
muscw.image(clip=0.05, legend=1)
plt.show()

#plt.show()

test = SUdata()
nr = 48
ns = 2501
dt = 0.0001
data = np.zeros((nr, ns), dtype=np.float32)
test.create(data, dt)
test.wind(tmin=0., tmax=0.1)
print(muscw.header[:])