# -*- coding: utf-8 -*-
"""
nessi.pso
================================================
"""
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

#from future.builtins import *

from .readpspace import readpspace

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
