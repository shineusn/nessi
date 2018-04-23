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
nessi_grd_vrn(const int npts, const int npar,
	      const float q[npts][npar],
	      const int n1, const int n2, const float dh,
	      float model[n1][n2][4])
{
  int i1, i2, ipts, imin;
  float x, z;
  float d, dmin;
    
  for(i2=0; i2<n2; i2++){
    for(i1=0; i1<n1; i1++){
      x = (float)(i2)*dh;
      z = (float)(i1)*dh;
      dmin = 0.;
      for(ipts=0; ipts<npts; ipts++){
	d = sqrt((x-q[ipts][0])*(x-q[ipts][0])			\
		 +(z-q[ipts][1])*(z-q[ipts][1]));
	if(ipts == 0){dmin = d; imin = ipts;}
	else{if(d < dmin){dmin = d; imin=ipts;}}
      }
      model[i1][i2][1] = q[imin][2];
      model[i1][i2][2] = q[imin][3];
      model[i1][i2][3] = q[imin][4];
      model[i1][i2][0] = 2.*q[imin][2];
    }
  }
    
  return;
  
}
