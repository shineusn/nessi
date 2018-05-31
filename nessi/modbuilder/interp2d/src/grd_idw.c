/* pso/nessi_grd_vrn.c
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

#include <nessi_grd.h>

void
nessi_grd_idw(const int npts,
	      const float xp[npts], const float zp[npts],
	      const float val[npts],
	      const int n1, const int n2, const float dh,
	      const int pw, float model[n1][n2])
{
  int i1, i2, ipts;
  float x, z, x2, z2, w, d;
  float den;
  float num;

  for(i2=0; i2<n2; i2++){
    x = ((float)i2)*dh;
    for(i1=0; i1<n1; i1++){
      z = ((float)i1)*dh;
      num = 0.;
      den = 0.;
      for(ipts=0; ipts<npts; ipts++){
	x2 = pow(x-xp[ipts], 2);
	z2 = pow(z-zp[ipts], 2);
	d = sqrt(x2+z2);
	if(pow(d, pw) > 0.){
	  w = 1./pow(d, pw);
	  num = num + w*val[ipts];
	  den = den + w;
	}
	else{
	  num = val[ipts];
	  den = 1.;
	}
      }
      model[i1][i2]=num/den;
    }
  }
  return;
}
