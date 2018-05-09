#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: subvalley_modeling.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Seismic modeling using the subvalley model.
:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from nessi.swm import modext, modbuo, modlame
from nessi.swm import acqpos, pmlmod
from nessi.swm import ricker, srcspread
from nessi.swm import evolution

from nessi.io import SUdata

def seismod(runpar, modpar, acqpar, vpmod, vsmod, romod):
    # ------------------------------------------------------------
    # >> Input parameters
    # ------------------------------------------------------------

    # >> Run parameters
    jobname = runpar['name']
    tmax = runpar['tmax']
    dt = runpar['dt']
    isnap = runpar['snap']
    dtsnap =  runpar['dtsnap']

    # >> Model grid parameters
    n1 = modpar['n1']
    n2 = modpar['n2']
    dh = modpar['dh']
    isurf = modpar['ifsurf']
    npml = modpar['npml']
    apml = modpar['apml']
    ppml = modpar['ppml']

    # >> Acquisition parameters
    acq = acqpar['acquisition']
    nrec = len(acq)
    dts = acqpar['dts']
    sx = acqpar['sx']
    sz = acqpar['sy']
    f0 = acqpar['f0']
    t0 = acqpar['t0']
    sigma = acqpar['spread']
    srctype = acqpar['type']


    # ------------------------------------------------------------
    # >> Calculate complementary parameters
    # ------------------------------------------------------------
    nt = int(tmax/dt)+1
    nts = int(tmax/dts+1)
    ntsnap = int(tmax/dtsnap)+1


    # ------------------------------------------------------------
    # >> Extent models
    # ------------------------------------------------------------

    vpe = modext(npml, vpmod)
    vse = modext(npml, vsmod)
    roe = modext(npml, romod)


    # ------------------------------------------------------------
    # >> Calculate buoyancy and Lame parameters
    # ------------------------------------------------------------

    bux, buz = modbuo(roe)
    mu, lbd, lbdmu = modlame(vpe, vse, roe)


    # ------------------------------------------------------------
    # >> Calculate PMLs
    # ------------------------------------------------------------

    pmlx0,pmlx1,pmlz0,pmlz1 = pmlmod(n1,n2,dh,isurf,npml,apml,ppml)


    # ------------------------------------------------------------
    # >> Generate input acquisition
    # ------------------------------------------------------------

    recpos = acqpos(n1, n2, npml, dh, acq)


    # ------------------------------------------------------------
    # >> Generate input source
    # ------------------------------------------------------------

    # >> Source spread grid
    gsrc = srcspread(n1, n2, npml, sx, sz, dh, sigma)

    # >> Ricker source
    tsrc = ricker(nt, dt, f0, t0)


    # ------------------------------------------------------------
    # >> Calculate stability condition
    # ------------------------------------------------------------

    #print("Courant:: ", dt*np.amax(vpe)/dh)


    # ------------------------------------------------------------
    # >> Marching
    # ------------------------------------------------------------

    recx,recz,recp = evolution(n1,n2,dh,npml,
                               nts,ntsnap,dt,srctype,
                               tsrc,gsrc,recpos,isurf,isnap,
                               bux,buz,lbd, lbdmu,mu,
                               pmlx0,pmlx1,pmlz0,pmlz1)

    # Minimal SU file
    surecz = SUdata()
    surecz.create(recz.swapaxes(1,0), dts)

    # Fill headers
    for ir in range(0, nrec):
        surecz.header[ir]['gx'] = acq[ir, 0]*10
        surecz.header[ir]['gy'] = acq[ir, 1]*10

    surecz.header[:]['sx'] = sx*10
    surecz.header[:]['gy'] = sz*10

    surecz.header['scalco'] = -10

    return surecz