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
nessi_grd_sib(const int npts,
	      const float xp[npts], const float zp[npts],
	      const float val[npts],
	      const int n1, const int n2, const float dh,
	      float model[n1][n2])
{
  int i1, i2, i2a, i2b, i1a, i1b, ipts, imin, ir, i1min, i1max, i2min, i2max;
  float x, z, xa, za, xb, zb;
  float d, dmin, v0, v1, v2, v3, n;
  float vrn[n1][n2];
  float cp[n1][n2], np[n1][n2];

  // VORONOI
  for(i2=0; i2<n2; i2++){
    for(i1=0; i1<n1; i1++){
      x = (float)(i2)*dh;
      z = (float)(i1)*dh;
      dmin = 0.;
      for(ipts=0; ipts<npts; ipts++){
	d = sqrt((x-xp[ipts])*(x-xp[ipts])+(z-zp[ipts])*(z-zp[ipts]));
	if(ipts == 0){dmin = d; imin = ipts;}
	else{if(d < dmin){dmin = d; imin=ipts;}}
      }
      vrn[i1][i2] = val[imin];
    }
  }

  // SIBSON
  for(i1a=0; i1a<n1; i1a++){
    for(i2a=0; i2a<n2; i2a++){
      cp[i1a][i2a] = 0.;
      np[i1a][i2a] = 0.;
    }
  }

  for(i2a=0; i2a<n2; i2a++){
    xa = (float)(i2a)*dh;
    for(i1a=0; i1a<n1; i1a++){
      za = (float)(i1a)*dh;
      dmin = 0.;
      for(ipts=0; ipts<npts; ipts++){
				d = sqrt((xa-xp[ipts])*(xa-xp[ipts])+(za-zp[ipts])*(za-zp[ipts]));
				if(ipts == 0){dmin = d; imin = ipts;}
				else{if(d < dmin){dmin = d; imin=ipts;}}
      }
      ir = (int)(dmin/dh)+1;
      i2min=i2a-ir;
      if(i2min < 0){i2min = 0;}
      i2max = i2a+ir;
      if(i2max > n2){i2max = n2;}
      i1min = i1a-ir;
      if(i1min < 0){i1min = 0;}
      i1max = i1a+ir;
      if(i1max > n1){i1max = n1;}
      for(i2b=i2min; i2b<i2max; i2b++){
				xb = (float)(i2b)*dh;
				for(i1b=i1min; i1b<i1max; i1b++){
	  			zb = (float)(i1b)*dh;
	  			d = sqrt((xa-xb)*(xa-xb)+(za-zb)*(za-zb));
	  if(d <= dmin){
	    cp[i1b][i2b] += vrn[i1a][i2a];
	    np[i1b][i2b] += 1.;
	  }
	}
      }
    }
  }
  for(i1a=0; i1a<n1; i1a++){
    for(i2a=0; i2a<n2; i2a++){
      model[i1a][i2a] = cp[i1a][i2a]/np[i1a][i2a];
    }
  }

  return;

}
