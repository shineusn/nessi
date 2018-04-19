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

// * Minimum between two integers
int
imin(const int a, const int b){if(a>b){return b;}else{return a;}}

// * Maximum between two integers
int
imax(const int a, const int b){if(a<b){return b;}else{return a;}}

// * Init 1D complex array to (0.+i0)
void
init1d_c( int n, float complex tab[n] ){
    for(int i=0; i<n; i++){tab[i] = (0. + 0. * _Complex_I) ;}
}
