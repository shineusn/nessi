# Modeling and inversion example

## Observed data
3 cores : 1 core per modeling

`mpiexec -n 3 python subvalley_modeling_mpi.py`

Output are SUfiles (vertical component only) in data folder

## Inversion using PSO
4 cores : 1 master and 1 slave per SUfile (modeling)

`mpiexec -n 4 python subvalley_inversion_mpi.py`

