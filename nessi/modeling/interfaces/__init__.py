# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: Convenience import for nessi.modeling.interfaces
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Initialization file for nessi.modeling.interfaces .

:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import nessi.modeling.interfaces classes and functions
from .gpdcwrap import dispersion_curve_init
from .gpdcwrap import dispersion_curve_rayleigh
from .gpdcwrap import dispersion_curve_love

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
