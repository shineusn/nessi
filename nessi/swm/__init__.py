# -*- coding: utf-8 -*-
"""
nessi.swm
================================================
"""
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from .swmwrap import modext, modbuo, modlame

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
