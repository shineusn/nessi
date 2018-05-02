import numpy as np
import matplotlib.pyplot as plt

from nessi.io import SUdata


musc = SUdata()

musc.read('musc_F50_01.su', endian='b')
musc.image()
plt.show()

musc.wind(tmin=0., tmax=0.25)
musc.image()
plt.show()