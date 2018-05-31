# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: Convenience import for nessi.globopt
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Initialization file for nessi.globopt.

:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import nessi.globopt classes and functions

from .pso import Swarm

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
