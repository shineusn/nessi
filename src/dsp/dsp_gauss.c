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

#include <nessi_dsp.h>

float
nessi_dsp_gauss (int iv, int iw, int nv, int nw, int
       igvmin, int igvmax, int igwmin, int igwmax,
       float gv[nv][nw], float gw[nv][nw],
       float sgv, float sgw, float disp[nv][nw] )
{

  int igv, igw ;
  float ev, ew, G ;
  float num=0, den=0 ;
  
  for( igw=(igwmin-1); igw<igwmax-1; igw++)
    {
      for( igv=igvmin-1; igv<igvmax-1; igv++ )
        {
	  ew = -0.5 * pow( ( gw[igv][igw] - gw[1][iw] ), 2 ) / ( sgw * sgw ) ;
	  ev = -0.5 * pow( ( gv[igv][igw] - gv[iv][1] ), 2 ) / ( sgv * sgv ) ;
	  G = exp( ew ) * exp( ev ) ;
	  num += fabs( disp[igv][igw] ) * G ;
	  den += G ;
        }
    }
  return (num/den) ;
  
}
