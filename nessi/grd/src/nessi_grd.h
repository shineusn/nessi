/* nessi_pso.h
 * 
 * Copyright (C) 2017, 2018 Damien Pageot
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __NESSI_GRD_H__
#define __NESSI_GRD_H__

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_rng.h>
#include <sys/time.h>

#include <complex.h>
#include <fftw3.h>

/*
   - nessi_grd_vrn()
   - nessi_grd_idw()
   - nessi_grd_ds1()
   - nessi_grd_ds2()
 */

void
nessi_grd_vrn(const int npts,
	      const float xp[npts], const float zp[npts],
	      const float val[npts],
	      const int n1, const int n2, const float dh,
	      float model[n1][n2]);

void
nessi_grd_idw(const int npts,
	      const float xp[npts], const float zp[npts],
	      const float val[npts],
	      const int n1, const int n2, const float dh,
	      const int pw, float model[n1][n2]);

void
nessi_grd_ds1(const int npts,
	      const float xp[npts], const float zp[npts],
	      const float val[npts],
	      const int n1, const int n2, const float dh,
	      float model[n1][n2]);

void
nessi_grd_ds2(const int npts,
	      const float xp[npts], const float zp[npts],
	      const float val[npts],
	      const int n1, const int n2, const float dh,
	      float model[n1][n2]);

#endif /* __NESSI_GRD_H_ */
