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
muscw.image(clip=0.5, legend=1)


#plt.show()