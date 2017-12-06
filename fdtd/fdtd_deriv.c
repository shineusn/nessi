/* fdtd/fdtd_deriv.c
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

#include <nessi_fdtd.h>

/*
 nessi_fdtd_dxforward ()
   Initialize particle positions with respect to parameter space boundaries

 Inputs:

 Return:
 */

void
nessi_fdtd_dxforward (const int n1, const int n2,
		      const float f[n1][n2], float d[n1][n2])
{
  float c1=(9./8.), c2=(-1./24.);
  
  for(unsigned int i2=1; i2<n2-2; i2++)
    {
      for(unsigned int i1=0; i1<n1; i1++)
	{
	  d[i1][i2] = c1*(f[i1][i2+1]-f[i1][i2])
	    + c2*(f[i1][i2+2]-f[i1][i2-1]);
	}
    }

  for(unsigned int i1=0; i1<n1; i1++)
    {
      d[i1][0] = f[i1][1]-f[i1][0];
      d[i1][n2-2] = f[i1][n2-1]-f[i1][n2-2];
    }
  return;
}


/*
 nessi_fdtd_dxbackward ()
   Initialize particle positions with respect to parameter space boundaries

 Inputs:

 Return:
 */

void
nessi_fdtd_dxbackward (const int n1, const int n2,
		       const float f[n1][n2], float d[n1][n2])
{
  float c1=(9./8.), c2=(-1./24.);
  
  for(unsigned int i2=2; i2<n2-1; i2++)
    {
      for(unsigned int i1=0; i1<n1; i1++)
	{
	  d[i1][i2] = c1*(f[i1][i2]-f[i1][i2-1])
	    + c2*(f[i1][i2+1]-f[i1][i2-2]);
	}
    }

  for(unsigned int i1=0; i1<n1; i1++)
    {
      d[i1][1] = f[i1][1]-f[i1][0];
      d[i1][n2-1] = f[i1][n2-1]-f[i1][n2-2];
    }
  return;
}
