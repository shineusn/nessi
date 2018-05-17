![NeSSI logo](https://raw.githubusercontent.com/wiki/PageotD/nessi/images/nessi.png)
![Powered by PYTHON](https://www.python.org/static/community_logos/python-powered-w-100x40.png)
![LGPL3 logo](https://www.gnu.org/graphics/lgplv3-88x31.png)

NeSSI (Near-Surface Seismic Imaging) aims to provide python modules for the rapid development of seismic inversion codes based on the particle swarm optimization method.

NeSSI is an open-source project licensed under the [LGPLv3]().

## Documentation

The [NeSSI wiki]() provides informations about:
* [installation]()
* [modeling engine]()
* [SU/CWP format]()
* [particle swarm optimization]()
* [contributing guide lines]()

The [NeSSI documentation]() gives technical informations about the NeSSI submodules, classes and functions.

Tutorials in the form of [jupyter notebooks]() will be available soon.

## Install
First, install git on your computer. For exemple on Ubuntu:

`sudo apt-get install git`

or use the `package manager`.

Then, in a terminal, go to the nessi/nessi folder and type:

`make`

Finally, you have to had the path of the nessi package to `PYTHONPATH`. In your `.bashrc` file, add:

`export PYTHONPATH=$PYTHONPATH:/path/to/the/nessi/package`

# Notebooks
[Particle Swarm Optimization](examples/particle_swarm/ParticleSwarmOptimization.md)
# Contributing

NeSSI is developed and tested using python2.7 and python3.5 on GNU/Debian Stretch (stable).

**Don't suffer from Shiny New Stuff Syndrome** -- [DontBreakDebian](https://wiki.debian.org/DontBreakDebian#Don.27t_suffer_from_Shiny_New_Stuff_Syndrome)
