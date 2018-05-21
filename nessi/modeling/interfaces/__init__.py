# -*- coding: utf-8 -*-
"""
nessi.swm
================================================
"""
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from .gpdcwrap import dispersion_curve_init
from .gpdcwrap import dispersion_curve_rayleigh
from .gpdcwrap import dispersion_curve_love

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
