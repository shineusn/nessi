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

void
nessi_dsp_gsmooth( int nv, int nw, float dv, float dw,
	 float v[nv], float w[nw], float sgv, float sgw,
	 float disp[nv][nw], float dispg[nv][nw])
{

  int iv, iw ;
  int iloc ;
  int igwmin, igwmax, igvmin, igvmax;
  float gw[nv][nw], gv[nv][nw] ;
  float G[nv][nw], aswap[nv][nw] ;
  float e1, e2 ;
  
  
  for( iv=0; iv<nv; iv++ )
    {
      for( iw=0; iw<nw; iw++ ){gw[iv][iw]=w[iw];gv[iv][iw]=v[iv];}
    }
  
  for( iw=0; iw<nw; iw++ )
    {
      iloc = (int)( ( ( gw[1][iw] - 3. * sgw ) - gw[1][1] ) / dw ) + 1 ;
      igwmin = imax( 1, iloc ) ;
      iloc = (int)( ( ( gw[1][iw] + 3. * sgw ) - gw[1][1] ) / dw ) + 1 ;
      igwmax = imin( nw, iloc ) ;
      
      for( iv=0; iv<nv; iv++ )
        {
	  iloc = (int)( ( ( gv[iv][1] - 3. * sgv ) - gv[1][1] ) / dv ) + 1 ;
	  igvmin = imax( 1, iloc ) ;
	  iloc = (int)( ( ( gv[iv][1] + 3. * sgv ) - gv[1][1] ) / dv ) + 1 ;
	  igvmax = imin( nv, iloc ) ;
	  
	  dispg[iv][iw] = nessi_dsp_gauss( iv, iw, nv, nw, igvmin, igvmax, igwmin, igwmax, gv, gw, sgv, sgw, disp ) ;
	  if(iv == 0){
	    dispg[iv][iw] = 0.;
	  }
        }
      //for(iw=0; iw<nw; iw++){
      //    dispg[0][iw] = dispg[1][iw];
      //}
    }
  return;
  
}
