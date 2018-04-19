/* pso/nessi_pso_updt.c
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

#include <nessi_pso.h>

/*
 nessi_pso_updt ()
   Check parameter space boundaries

 Inputs:
   - x: value to be tested
   - xmin, xmax: minimum and maximum values

 Return:
   - x if xmin < x < xmax
   - xmin if x < xmin
   - xmax if x > xmax
 */

void
nessi_pso_updt (const int nindv, const int npts, const int npar,
	  const float ql[nindv][npts][npar],
	  const float qg[npts][npar], const float modinit[npts][npar][3],
	  const float c0, const float c1, const float c2, const int constrict,
	  float q[nindv][npts][npar], float v[nindv][npts][npar])
{
    float cp = 0., cg = 0.;
    float r1 = 0., r2 = 0.;
    
    /* Inertia or constriction */
    if (constrict == 0)
      {
	/* inertia weight approach */
	cp = c1;
	cg = c2;
      }
    else
      {
	/* constriction factor approach */
	cp = c0*c1;
	cg = c0*c2;
      }

    /* Update process */
    for (unsigned int indv=0; indv<nindv; indv++)
      {
        for (unsigned int ipts=0; ipts<npts; ipts++)
	  {
            for (unsigned int ipar=0; ipar<npar; ipar++)
	      {
                /* Trial */
                r1 = nessi_randgsl();
		r2 = nessi_randgsl();
                while (r1 == r2)
		  {
		    r1 = nessi_randgsl();
		    r2 = nessi_randgsl();
		  }
		
                /* Update particle velocity */
                v[indv][ipts][ipar] = c0*v[indv][ipts][ipar]+
		  cp*r1*(ql[indv][ipts][ipar]-q[indv][ipts][ipar])+
		  cg*r2*(qg[ipts][ipar]-q[indv][ipts][ipar]);

		/* Check particle velocity */
		/* If absolute value of v is greater than vmax */
		if (abs(v[indv][ipts][ipar])>modinit[ipts][ipar][2])
		  {
		    v[indv][ipts][ipar] =
		      copysign (modinit[ipts][ipar][2],
				v[indv][ipts][ipar]);
		  }
		
                /* Update particle position */
                q[indv][ipts][ipar] += v[indv][ipts][ipar];
		
		/* Check boundaries */
                q[indv][ipts][ipar] = nessi_pso_bound(q[indv][ipts][ipar],
						      modinit[ipts][ipar][0],
						      modinit[ipts][ipar][1]);
            }
	  }    
      }    
    
    return;
}
