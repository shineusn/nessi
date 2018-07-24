# -------------------------------------------------------------------
# Filename: grdinterp.pyx
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Functions for coarse grid to fine grid interpolation.

:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""
import numpy as np
cimport numpy as np
cimport cython

ctypedef np.float DTYPE_f

@cython.boundscheck(False)
@cython.wraparound(False)

def grdvoronoi(int npts, np.ndarray[float, ndim=1] xp, np.ndarray[float, ndim=1] zp, np.ndarray[float, ndim=1] val, int n1, int n2, float dh):
    """
    Coarse inversion gird to fine modelling grid using Voronoi tesselation.
    """

    cdef Py_ssize_t i1, i2, ipts
    cdef int imin
    cdef float x, z, d, dmin

    # Initialize output fine grid
    cdef np.ndarray[float, ndim=2] model = np.zeros((n1, n2), dtype=np.float32)
    cdef np.ndarray[float, ndim=1] dist = np.zeros(npts, dtype=np.float32)

    # Loop over x-axis
    for i2 in range(0, n2):
      # Calculate position in x
      x = float(i2)*dh
      # Loop over z-axis
      for i1 in range(0, n1):
        # Calculate position in z
        z = float(i1)*dh
        # Get the closest point
        dist[:] = np.sqrt((x-xp[:])*(x-xp[:])+(z-zp[:])*(z-zp[:]))
        imin = np.argmin(dist)
        # Attribute value
        model[i1, i2] = val[imin]

    return model

def grdinvdist(int npts, np.ndarray[float, ndim=1] xp, np.ndarray[float, ndim=1] zp, np.ndarray[float, ndim=1] val, int n1, int n2, float dh, int pw):
  """
  Coarse inversion gird to fine modelling grid using inverse distance weighting interpolation.
  """

  cdef Py_ssize_t i1, i2, ipts
  cdef float x, z, num, den, w

  # Initialize output fine grid
  cdef np.ndarray[float, ndim=2] model = np.zeros((n1, n2), dtype=np.float32)
  cdef np.ndarray[float, ndim=1] dist = np.zeros(npts, dtype=np.float32)

  # Loop over x-axis
  for i2 in range(0, n2):
    x = float(i2)*dh
    # Loop over z-axis
    for i1 in range(0, n1):
      z = float(i1)*dh
      # Initialize num and den
      num = 0.
      den = 0.
      # Calulate distsance
      dist[:] = np.sqrt((x-xp[:])*(x-xp[:])+(z-zp[:])*(z-zp[:]))
      # Loop over points
      for ipts in range(0, npts):
        if dist[ipts] > 0.:
          w = 1./np.power(dist[ipts], pw)
          num += w*val[ipts]
          den += w*val[ipts]
        else:
          num = val[ipts]
          den = 1.
      model[i1, i2] = num/den

  return model

def grdsibson(int npts, np.ndarray[float, ndim=1] xp, np.ndarray[float, ndim=1] zp, np.ndarray[float, ndim=1] val, int n1, int n2, float dh):
  """
  Coarse inversion gird to fine modelling grid using a simplify discrete Sibson interpolation.
  """

  cdef Py_ssize_t i1a, i2a, i1b, i2b, ipts, i1min, i1max, i2min, i2max
  cdef int imin, ir
  cdef float xa, za, xb, zb, d, dmin, cp, nump

  # Initialize the Voronoi model
  cdef np.ndarray[float, ndim=2] vrn = np.zeros((n1, n2), dtype=np.float32)

  # Initialize the radius map
  cdef np.ndarray[float, ndim=2] radius = np.zeros((n1, n2), dtype=np.float32)

  # Initialize output fine grid
  cdef np.ndarray[float, ndim=2] model = np.zeros((n1, n2), dtype=np.float32)
  cdef np.ndarray[float, ndim=1] dist = np.zeros(npts, dtype=np.float32)

  # Calculate the Voronoi model
  vrn = grdvoronoi(npts, xp, zp, val, n1, n2, dh)

  # Calculate the radius
  for i2 in range(0, n2):
    x = float(i2)*dh
    for i1 in range(0, n1):
      z = float(i1)*dh

  # Process
  for i2b in range(0, n2):
    xb = float(i2b)*dh
    for i1b in range(0, n1):
      zb = float(i1b)*dh
      # Calulate distsance
      dist[:] = np.sqrt((xb-xp[:])*(xb-xp[:])+(zb-zp[:])*(zb-zp[:]))
      # Get the min distance
      imin = np.argmin(dist)
      dmin = dist[imin]
      # Calculate the radius in term of points
      ir = int(dmin/dh)+1
      # Determine min and max indices
      i1min = max(0, i1b-ir)
      i1max = min(n1, i1b+ir)
      i2min = max(0, i2b-ir)
      i2max = min(n2, i2b+ir)
      cp = 0.
      nump = 0.
      for i2a in range(i2min, i2max):
        xa = float(i2a)*dh
        for i1a in range(i1min, i1max):
          za = float(i1a)*dh
          if np.sqrt((xa-xb)*(xa-xb)+(za-zb)*(za-zb)) < dmin:
            cp += vrn[i1a, i2a]
            nump += 1.

      # Calculate finale model
      model[i1b, i2b] = cp/nump

  return model
