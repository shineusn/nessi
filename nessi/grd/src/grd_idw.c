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
nessi_grd_idw(const int npts, const int npar,
	      const float q[npts][npar],
	      const int n1, const int n2, const float dh,
	      const int pw, float model[n1][n2][4])
{
  int i1, i2, ipts, ipar;
  float x, z, x2, z2, w, d;
  float den;
  float num[npar];

  for(i2=0; i2<n2; i2++){
    x = ((float)i2)*dh;
    for(i1=0; i1<n1; i1++){
      z = ((float)i1)*dh;
      for(ipar=0; ipar<npar; ipar++){num[ipar]=0.;}
      den = 0.;
      for(ipts=0; ipts<npts; ipts++){
	x2 = pow(x-q[ipts][0], 2);
	z2 = pow(z-q[ipts][1], 2);
	d = sqrt(x2+z2);
	if(pow(d, pw) > 0.){
	  w = 1./pow(d, pw);
	  num[1] = num[1] + w*q[ipts][2];
	  num[2] = num[2] + w*q[ipts][3];
	  num[3] = num[3] + w*q[ipts][4];
	  den = den + w;
	}
	else{
	  num[1] = q[ipts][2];
	  num[2] = q[ipts][3];
	  num[3] = q[ipts][4];
	  den = 1.;
	}
      }
      model[i1][i2][1]=num[1]/den;
      model[i1][i2][2]=num[2]/den;
      model[i1][i2][3]=num[3]/den;
      model[i1][i2][0] = 2.*model[i1][i2][1];
    }
  }
  return;
}
