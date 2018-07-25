# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: Convenience import for nessi.modbuilder
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Initialization file for nessi.modbuilder .

:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import nessi.modbuilder.interp2d classes and functions
from .interp2d.grdwrap import voronoi
from .interp2d.grdwrap import idweight
from .interp2d.grdwrap import sibson

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
