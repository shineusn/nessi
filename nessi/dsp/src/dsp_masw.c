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
nessi_dsp_masw(int nv, int nw, int n1c, int ns,
	       int nr, int iwmin, float v[nv], float w[nw],
	       float dist[ns][nr], float complex dobsc[n1c][nr],
	       float disp[nv][nw])
{

  unsigned int iv, iw, is, ir ;
  float phs ;
  float complex ci = 0. + 1.0 * _Complex_I ;
  float complex tmp[nw] ;
  
  for(iv=0; iv<nv; iv++)
    {
      init1d_c(nw, tmp) ;
      for(is=0; is<ns; is++){for(ir=0; ir<nr; ir++){for(iw=0; iw<nw; iw++)
	    {
	      if(cabs(dobsc[iwmin+iw][(is)*nr+ir]) != 0.)
		{phs=nessi_dsp_phase(w[iw],dist[is][ir],v[iv]);
		  tmp[iw]+=dobsc[iwmin+iw][ir]*cexp(ci*phs);
		};
	    }
	}
      }
      for(iw=0;iw<nw;iw++){disp[iv][iw]+=cabs(tmp[iw]);}
    }
  return;
  
}
