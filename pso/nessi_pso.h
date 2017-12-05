/* nessi_pso.h
 * 
 * Copyright (C) 2017 Damien Pageot
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

#ifndef __NESSI_PSO_H__
#define __NESSI_PSO_H__

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_rng.h>
#include <sys/time.h>

#include <complex.h>
#include <fftw3.h>

/*
   - randgsl()
   - randpar()
   - nessi_init_swarm()
 */
 
float 
nessi_randgsl ();

float 
nessi_randpar (const float pmin, const float pmax);

float
nessi_pso_bound (const float x, const float xmin, const float xmax);

void
nessi_pso_init (const int nindv, const int npts, const int npar,
		  const float modinit[npts][npar][2],
		  float q[nindv][npts][npar]);

void
nessi_pso_updt (const int nindv, const int npts, const int npar,
	  const float ql[nindv][npts][npar],
	  const float qg[npts][npar], const float modinit[npts][npar][2],
	  const float c0, const float c1, const float c2, const int constrict,
		float q[nindv][npts][npar], float v[nindv][npts][npar]);

#endif /* __NESSI_PSO_H_ */
