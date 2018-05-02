import numpy as np
import matplotlib.pyplot as plt

from nessi.io import SUdata


musc = SUdata()

musc.read('musc_F50_01.su', endian='b')

plt.imshow(musc.data[:]['trace'], aspect='auto', cmap='gray')
plt.show()

plt.plot(musc.data[20]['trace'])
plt.show()
