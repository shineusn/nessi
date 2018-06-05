# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2018-06-05

### Added
- *CHANGELOG.md* in docs/
- *Interface with Geopsy-gpdc* in docs/
- *Particle Swarm Optimization: basics* in docs/
- *Read, write and create SU data* tutorial in docs/
- *Windowing SU data* tutorial in docs/
- *Tapering SU data* tutorial in docs/
- **lib** folder for future C/Fortran libraries
- *nessi.modeling.swm references* in docs/
- *nessi.globopt references* in docs
- *MASW from SU data* tutorial in docs/
- *masw* method in *SU/CWP references* chapter in docs/
- *Dispersion curve inversion using GPDC and PSO* tutorial in docs/

### Modified
- add __ZENODO__ DOI in the README.md
- interfaces references documentation
- *Seismic modeling example* now in tutorials
- *SU/CWP references* now in *NeSSI API* chapter
- *Getting started* chapter in docs/

### Fixed
- *wind* method of SUdata() can now apply a window in time and space at the same time.
- *pfilter* method of SUdata() can now handle axis 0 and 1
- *masw* method of SUdata() can now return freq and vel arrays as expected
- *masw* method of SUdata() now handles correctly the *scalco* keyword

## Removed
- *2D seismic modeling* part in docs/ (temporary)

## [0.1.1] - 2018-06-01

### Added
- *test_windowing.py* in nessi/signal/tests
- *test_tapering.py* in nessi/signal/tests
- *test_filtering.py* in nessi/signal/tests

### Modified
- README.md

### Fixed
- remake html documentation
- *signal.time_window* issue for 1D signal
- *signal.taper1d* issue for 1D signal

## [0.1.0] - 2018-05-31

### Added
- CONTRIBUTE.md
- *getting started* chapter in docs/
- *interfaces* chapter in docs/
- *gprMax* paragraph in *interfaces* (docs/)
- *interfaces references* chapter in docs
- *geopsy-gpdc* paragraph in *interfaces* (docs/)
- geopsy-gpdc interface in nessi.modeling.interfaces
- *test_gpdcwrap.py* in nessi/modeling/tests
- *NeSSI Global Optimization* references (docs/)
- *test_swarm.py* in nessi/globopt/tests
- *SU/CWP references* (docs/)
- time_window function in nessi.signal windowing.py
- space_window function in nessi.signal windowing.py
- taper1d function in nessi.signal tapering.py
- sine and cosine taper types
- sin2filter polynomial filter nessi.signal filtering.py
- pfilter method in nessi.io for SU data format
- adding taper method in nessi.io for SU data format
- adding kill method (zero out traces) in nessi.io for SU data format
- add *modbuilder* module (perspectives)

### Modified
- README.md
- nessi.swm functions are now located at nessi.modeling.swm
- nessi.pso.Swarm class is now callable from nessi.globopt.Swarm
- adding window in space to suwind method in nessi.io for SU data format
- wind method (SU format) now depends nessi.signal.time_window and nessi.signal.space_window
- all *__init__.py headers*
- all python file headers (docstrings...)
- all Fortran source code headers (infos)
- rename *grd* module in *interp2d* and move it in *modbuilder* module

### Fixed
- *get_gbest* method of the Swarm class (nessi.globopt), option *ring*

## [0.0.0] - 2018-05-21
- starting point for development of the true first version (0.1.0); not a valid version.

## [X.X.X] - YYYY-MM-DD
### Added
### Fixed
### Removed
