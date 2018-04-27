import numpy as np
import matplotlib.pyplot as plt

from nessi.swm import modext, modbuo, modlame
from nessi.swm import acqpos, pmlmod
from nessi.swm import ricker, srcspread
#from nessi.swm import evolution


# ------------------------------------------------------------
# >> Input parameters
# ------------------------------------------------------------

# >> Run parameters
jobname = 'test'
tmax = 1.0
dt = 0.0001

# >> Grid dimensions and node spacing
n1 = 51
n2 = 301
dh = 0.5

# >> Boundaries parameters
isurf = 1 # Free surface
npml = 20  # width in points of the PML bands
apml = 6000.
ppml = 32

# >> Acquisition parameters
nrec = 48
drec = 2.0
xrec0 = 28.
zrec0 = dh
dts = 0.0001

# >> Source parameters
xs = 10.0; zs = 0.5 # source position
f0 = 15.0; t0 = 0.1 # peak frequency and t0
sigma = -1.
srctype = 2

# >> Snapshots
isnap = 0
dtsnap = 0.001


# ------------------------------------------------------------
# >> Calculate complementary parameters
# ------------------------------------------------------------
nt = int(tmax/dt)+1
nts = int(tmax/dts+1)
ntsnap = int(tmax/dtsnap)+1


# ------------------------------------------------------------
# >> Generate input homogeneous models
# ------------------------------------------------------------

vp = np.zeros((n1, n2), dtype=np.float32)
vs = np.zeros((n1, n2), dtype=np.float32)
ro = np.zeros((n1, n2), dtype=np.float32)

vp[:, :] = 600.  # m/s
vs[:, :] = 200.  # m/s
ro[:, :] = 1500. # kg/m3


# ------------------------------------------------------------
# >> Extent models
# ------------------------------------------------------------

vpe = modext(npml, vp)
vse = modext(npml, vs)
roe = modext(npml, ro)


# ------------------------------------------------------------
# >> Calculate buoyancy and Lame parameters
# ------------------------------------------------------------

bux, buz = modbuo(roe)
mu0, mue, lb0, lbmu = modlame(vpe, vse, roe)


# ------------------------------------------------------------
# >> Calculate PMLs
# ------------------------------------------------------------

pmlx0,pmlx1,pmlz0,pmlz1 = pmlmod(n1,n2,dh,isurf,npml,apml,ppml,vpe)


# ------------------------------------------------------------
# >> Generate input acquisition
# ------------------------------------------------------------

acq = np.zeros((nrec, 2), dtype=np.float32)
for irec in range(0, nrec):
    acq[irec,0] = xrec0+float(irec)*drec
    acq[irec,1] = zrec0

recpos = acqpos(n1, n2, npml, dh, acq)


# ------------------------------------------------------------
# >> Generate input source
# ------------------------------------------------------------

# >> Source spread grid
gsrc = srcspread(n1, n2, npml, xs, zs, dh, sigma)

# >> Ricker source
tsrc = ricker(nt, dt, f0, t0)


# ------------------------------------------------------------
# >> Calculate stability condition
# ------------------------------------------------------------

print "Courant:: ", dt*np.amax(vpe)/dh


# ------------------------------------------------------------
# >> Marching
# ------------------------------------------------------------




# ------------------------------------------------------------
# >> Plot seismograms
# ------------------------------------------------------------
