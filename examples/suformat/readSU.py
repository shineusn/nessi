import numpy as np
import matplotlib.pyplot as plt

from nessi.io import SUdata


musc = SUdata()

musc.read('musc_F50_01.su')
plt.subplot(121)
musc.image()

#print(musc.header[0]['ns'].flags)
musc.wind(tmin=-0.0, tmax=0.3)
plt.subplot(122)
musc.image()

#plt.show()