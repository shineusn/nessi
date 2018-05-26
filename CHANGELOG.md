# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.1.0] - YYYY-MM-DD

### Added
- geopsy-gpdc interface in nessi.modeling.interfaces
- *interfaces* chapter in docs/
- *interfaces references* chapter in docs
- *geopsy-gpdc* paragraph in *interfaces* (docs/)
- *gprMax* paragraph in *interfaces* (docs/)
- *NeSSI Global Optimization* references (docs/)
- *SU/CWP references* (docs/)
- time_window function in nessi.signal windowing.py
- space_window function in nessi.signal windowing.py
- taper1d function in nessi.signal tapering.py
- sine and cosine taper types
- SU/CWP class references in docs/
- sin2filter polynomial filter nessi.signal filtering.py
- pfilter method in nessi.io for SU data format
- adding taper method in nessi.io for SU data format
- adding kill method (zero out traces) in nessi.io for SU data format

### Modified
- README.md
- nessi.swm functions are now located at nessi.modeling.swm
- nessi.pso.Swarm class is now callable from nessi.globopt.Swarm
- adding window in space to suwind method in nessi.io for SU data format
- wind method (SU format) now depends nessi.signal.time_window and nessi.signal.space_window

## [0.0.0] - 2018-05-21
- starting point for development

## [X.X.X] - YYYY-MM-DD
### Added
### Fixed
### Removed
