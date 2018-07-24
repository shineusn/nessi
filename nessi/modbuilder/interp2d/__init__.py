# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: Convenience import for nessi.modbuilder.interp2d
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Initialization file for nessi.modbuilder.interp2d .

:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import nessi.grd classes and functions
from .grdwrap import voronoi
from .grdwrap import idweight
from .grdwrap import sibson1
from .grdwrap import sibson2

from .grdinterp import grdvoronoi 
from .grdinterp import grdinvdist
from .grdinterp import grdsibson

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
