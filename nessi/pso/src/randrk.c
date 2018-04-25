/* pso/nessi_randgsl.c
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

float
nessi_randrk(){
  rk_state state;
  unsigned long seed = 1;
  double random_value;
  
  rk_seed(seed, &state); // Initialize the RNG
  random_value = rk_double(&state); // Generate random values in [0..RK_MAX]
  return (float)random_value;
}
