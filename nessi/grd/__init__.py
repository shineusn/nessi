# -*- coding: utf-8 -*-
"""
nessi.grd
================================================
"""
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from .grdwrap import voronoi, idweight, sibson1, sibson2

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
