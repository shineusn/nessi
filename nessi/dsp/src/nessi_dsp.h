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

#ifndef __NESSI_DSP_H__
#define __NESSI_DSP_H__

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

float
nessi_dsp_phase(const float w,const float d, const float v);

void
nessi_dsp_masw (int nv, int nw, int n1c, int ns,
	       int nr, int iwmin, float v[nv], float w[nw],
	       float dist[ns][nr], float complex dobsc[n1c][nr],
	       float disp[nv][nw]);

float
nessi_dsp_gauss (int iv, int iw, int nv, int nw,
		 int igvmin, int igvmax, int igwmin, int igwmax,
		 float gv[nv][nw], float gw[nv][nw],
		 float sgv, float sgw, float disp[nv][nw] );

void
nessi_dsp_gsmooth( int nv, int nw, float dv, float dw,
	 float v[nv], float w[nw], float sgv, float sgw,
	 float disp[nv][nw], float dispg[nv][nw]);

// * Minimum between two integers
int
imin(const int a, const int b);

// * Maximum between two integers
int
imax(const int a, const int b);

void
init1d_c( int n, float complex tab[n] );

#endif /* __NESSI_DSP_H_ */
