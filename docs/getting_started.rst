***************
Getting started
***************

NeSSI is currently developed under 64-bit GNU/Linux distributions only (Debian 9 Stretch and Ubuntu 16.10) using virtual environments created with `Miniconda <https://conda.io/miniconda.html>`_. NeSSI is designed to run with some of the major Python releases (2.7, 3.4, 3.5 and 3.6) since all users doesn't have access to the latest version.

If you want to use a specific release of Python which is not supported by your OS, we strongly recommand to create a virtual environment using `Miniconda <https://conda.io/miniconda.html>`_ instead of manually installing Python from sources on your system (`Don't suffer from Shiny New Stuff Syndrome - Don't break Debian <https://wiki.debian.org/DontBreakDebian#Don.27t_suffer_from_Shiny_New_Stuff_Syndrome>`_).

============
Dependencies
============

NeSSI requiered:

* a C and a Fortran compiler such as `GCC <https://gcc.gnu.org/>`_
* the **Numpy** python package
* the **Scipy** python package
* the **Matplotlib** python package

All can be installed using your package manager and/or the Python **pip** package manager.

============
Installation
============

The installation of NeSSI is not automatized yet (with a setup.py for example) but it is quite simple.

In a terminal, in the nessi folder, type to compile C and Fortran libraries:  ``make`` .

Then, you have to add the path of the nessi package to ``PYTHONPATH``. In your ``.bashrc`` file, add:

``export PYTHONPATH=$PYTHONPATH:/path/to/the/nessi/package``

Regenerate all pathes: ``source ~/.bashrc``.

NeSSI package is now available from python.

-----------
Geopsy-gpdc
-----------

If you want to use the Geopsy-gpdc interfaces, you must have ``gpdc`` installed on your computer and you have to edit the path to QGpCore library (provided during the Geopsy compilation) in ``nessi/__init__.py``.
