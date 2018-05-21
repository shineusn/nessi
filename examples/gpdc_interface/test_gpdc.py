import numpy as np
import matplotlib.pyplot as plt

from nessi.modeling.interfaces import dispersion_curve_init
from nessi.modeling.interfaces import dispersion_curve_rayleigh

dispersion_curve_init(1)

nLayers = 3
h = np.zeros(nLayers, dtype=np.float64)
vp = np.zeros(nLayers, dtype=np.float64)
vs = np.zeros(nLayers, dtype=np.float64)
rho = np.zeros(nLayers, dtype=np.float64)

h[0] = 7.5
h[1] = 25.0
vp[0] = 500.0
vp[1] = 1350.0
vp[2] = 2000.0
vs[0] = 200.0
vs[1] = 210.0
vs[2] = 1000.0
rho[0] = 1800.0
rho[1] = 1900.0
rho[2] = 2500.0

# Frequency sample
nSamples = 51
omega = np.linspace(10., 50., 51)
omega *= 2.*np.pi

nModes = 1
slowness = np.zeros((nSamples*nModes), dtype=np.float64)
group = 0

dispersion_curve_rayleigh(nLayers, h, vp, vs, rho, nSamples, omega, nModes, slowness, group)

plt.plot(slowness)
plt.show()
