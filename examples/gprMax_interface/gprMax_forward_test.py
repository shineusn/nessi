# TODO:
# - test gprMax forward problem [X]
# - test read output data [X]
# - create a function to write the input file
# - test PSO -> size and position of the cylinder / waveform inversion

import h5py
import gprMax
import sys
import numpy as np
import matplotlib.pyplot as plt
#sys.stdout = open('file', 'w')


def create_gprmax_input(x, y, r):
    """
    Create a simple input copy from Bscan example where
    only the cylinder is edited
    """
    gprinput = open('gprmax_input.in', 'w')

    # title
    gprinput.write('#title: B-scan from a metal cylinder buried in a dielectric half-space\n')
    # domain
    gprinput.write('#domain: 0.240 0.210 0.002\n')
    # dx dy dz
    gprinput.write('#dx_dy_dz: 0.002 0.002 0.002\n')
    # time window
    gprinput.write('#time_window: 3e-9\n\n')
    # materials
    gprinput.write('#material: 6 0 1 0 half_space\n\n')
    # waveform
    gprinput.write('#waveform: ricker 1 1.5e9 my_ricker\n')
    # hertzian dipole
    gprinput.write('#hertzian_dipole: z 0.040 0.170 0 my_ricker\n')
    # rx
    gprinput.write('#rx_array: 0.080 0.170 0 0.160 0.170 0 0.010 0 0 \n')
    # src step
    gprinput.write('#src_steps: 0.010 0 0\n')
    # rx step
    #gprinput.write('#rx_steps: 0.010 0 0\n\n')
    # box
    gprinput.write('#box: 0 0 0 0.240 0.170 0.002 half_space\n')
    # cylinder
    gprinput.write('#cylinder: '+str(x)+' '+str(y)+' 0 '+str(x)+' '+str(y)+' 0.002 '+str(r)+' pec\n')

    gprinput.close()



n=1

# position and radius of the cylinder
x = 0.120
y = 0.080
r = 0.010

# Create the input file
create_gprmax_input(x, y, r)

# Run gprMax
run_name = 'gprmax_input'
gprMax.run(run_name+'.in', n=n)

# Plot results
plt.subplot(131)
plt.title(r'Ez')
for i in range(0, n):
    gprout = h5py.File(run_name+'.out', 'r')
    n1 = gprout.get('/rxs/rx1/Ez')
    n2 = gprout.get('/rxs/rx2/Ez')
    n1 = np.array(n1)
    n2 = np.array(n2)
    plt.plot(n1)
    plt.plot(n2)

plt.subplot(132)
plt.title(r'Hx')
for i in range(0, n):
    gprout = h5py.File(run_name+'.out', 'r')
    #n1 = gprout.get('/rxs/rx1/Ez')
    n1 = gprout.get('/rxs/rx1/Hx')
    n1 = np.array(n1)
    plt.plot(n1)

plt.subplot(133)
plt.title(r'Hy')
for i in range(0, n):
    gprout = h5py.File(run_name+'.out', 'r')
    #n1 = gprout.get('/rxs/rx1/Ez')
    n1 = gprout.get('/rxs/rx1/Hy')
    n1 = np.array(n1)
    plt.plot(n1)

plt.show()
