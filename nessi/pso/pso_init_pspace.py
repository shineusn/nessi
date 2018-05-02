"""
Module pso_init_pspace.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import loadtxt, zeros, float32


def pso_init_pspace(fmod):
    """
    Create a table containing the parameter space boundaries.

    Args:
        fmod (str): file containing the parameter space values.

    Returns:
        array of floats: array containing the parameter space values.
    """

    # Load pspace file in a temporary array
    tmp = loadtxt(fmod, ndmin=2, comments='#')

    # Check the number of points per particule
    try:
        npts = tmp.shape[0]
        npar = int(tmp.shape[1]/3)
    except IndexError:
        npts = 1
        npar = int(tmp.shape[0]/3)

    # Initialize pspace array
    pspace = zeros((npts, npar, 3), dtype=float32)

    # Fill pspace array
    i = 0
    if npts == 1:
        for ipar in range(0, npar):
            pspace[0, ipar, :] = tmp[i:i+3]
            i += 3
    else:
        for ipar in range(0, npar):
            pspace[:, ipar, :] = tmp[:, i:i+3]
            i += 3

    return pspace
