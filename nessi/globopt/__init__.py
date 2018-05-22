# -*- coding: utf-8 -*-
"""
nessi.globopt

A module containing class for particle swarm
optimization.
================================================
"""
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from .pso import Swarm

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
