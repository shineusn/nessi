/* swm/nessi_swm_modext.c
 * 
 * Copyright (C) 2018 Damien Pageot
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

#include <nessi_swm.h>

void
nessi_swm_modext (const int n1, const int n2, const int npml,
		  float v[n1][n2], float ve[n1+2*npml][n2+2*npml])
{
  int i1, i2, ipml;

  // Fill extend model with the original model
  for(i2=0;i2<n2;i2++)
    {
      for(i1=0;i1<n1;i1++)
	{
	  ve[i1+npml][i2+npml] = v[i1][i2];
	}
    }

  // Fill left and right PML areas
  for(i1=0; i1<n1; i1++)
    {
      for(ipml=0;ipml<npml;ipml++)
	{
	  ve[i1+npml][ipml] = v[i1][0];
	  ve[i1+npml][n2+npml+ipml] = v[i1][n2-1];
	}
    }
  
  // Fill top and bottom PML areas
  for(i2=0; i2<n2+2*npml; i2++)
    {
      for(ipml=0;ipml<npml;ipml++)
	{
	  ve[ipml][i2] = ve[npml][i2];
	  ve[n1+npml+ipml][i2] = ve[n1+npml-1][i2];
	}
    }
  
  return;
}

