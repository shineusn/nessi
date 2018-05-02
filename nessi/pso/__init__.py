# -*- coding: utf-8 -*-
"""
nessi.pso
================================================
"""
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from .pso_init_pspace import pso_init_pspace as init_pspace
from .pso_standard import pso_standard_update as standard_update
from .pso_init_swarm import pso_init_swarm as init_swarm
from .particle_class import particles
from .swarm import Swarm

if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
