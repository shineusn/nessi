/* pso/pso_bound.c
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

#include <nessi_pso.h>

/*
 initswarm()
   Check parameter space boundaries

 Inputs:
   - x: value to be tested
   - xmin, xmax: minimum and maximum values

 Return:
   - x if xmin < x < xmax
   - xmin if x < xmin
   - xmax if x > xmax
 */

float
nessi_pso_bound (const float x, const float xmin, const float xmax)
{
    if(x < xmin)
      {
	return xmin;
      }
    else{
      if(x > xmax)
	{
	  return xmax;
	}
      else
	{
	  return x;
	}
    }
}
