# -*- coding: utf-8 -*-
"""
nessi.dsp
================================================
"""
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from .dspwrap import maswfv, smooth

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
