
Particle Swarm Optimization: basics
===================================

.. code:: ipython3

    # Import matplotlib and numpy modules
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # Import the Swarm class from NeSSI
    from nessi.globopt import Swarm

.. code:: ipython3

    def peaksF(X, Y):
        F = 3.*(1.-X)*(1.-X)\
                    *np.exp(-1.*X**2-(Y+1.)**2)\
                    -10.*(X/5.-X**3-Y**5)\
                    *np.exp(-1.*X**2-Y**2)\
                    -1./3.*np.exp(-1.*(X+1)**2-Y**2)

        return F

.. code:: ipython3

    # Initialize 3D plot
    fig = plt.figure(figsize=(9,6))
    ax = fig.gca(projection='3d')
    ax.set_xlabel(r'$x_{1}$')
    ax.set_ylabel(r'$x_{2}$')
    ax.set_zlabel(r'Amplitude')

    # Calculate peak function
    X, Y = np.meshgrid(np.linspace(-3, 3, 61), np.linspace(-3, 3, 61))
    F = peaksF(X, Y)

    # Plot
    ax.plot_surface(X, Y, F, vmin=-6.0, vmax=8.0, cmap='jet');



.. image:: images/pso_basics_01.png


The search-space is delimited by the minimum and maximum values of each
parameter (x1 and x2 in this case). An increment value (dx) is added to
control the maximum displacement of the swarm's particles.

+----------+----------+-------+----------+----------+-------+
| x1 min   | x1 max   | dx1   | x2 min   | x2 max   | dx2   |
+==========+==========+=======+==========+==========+=======+
| -3.0     | 3.0      | 0.3   | -3.0     | 3.0      | 0.3   |
+----------+----------+-------+----------+----------+-------+

.. code:: ipython3

    # Initialize the swarm object
    swarm = Swarm()

    # PSO parameters
    ngen = 100
    nindv = 20
    fit = np.zeros((ngen+1, 2), dtype=np.float32)

    # Get the search-space
    # Alternatively, the search space can be loaded from a text file using the function
    #     swarm.init_pspace('name_of_the_file')
    # The file must be formatted as follow:
    # - one line per point
    # - for each line: x1min, x1max, dx1, ..., xNmin, xNmax, dxN
    # - comments='#'
    # Here, only one point is searched: the one for which the two parameters (X, Y)
    # gives the minimum value of the 2D peak function.
    swarm.pspace = np.array([[[-3.0, 3.0, 0.3],
                              [-3.0, 3.0, 0.3]]],
                            dtype=np.float32)

    # Initialize particles
    swarm.init_particles(nindv)

.. code:: ipython3

    # First evaluation
    swarm.misfit[:] = peaksF(swarm.current[:, 0, 0], swarm.current[:, 0, 1])
    fit[0, 0] = np.amin(swarm.misfit)
    fit[0, 1] = np.mean(swarm.misfit)

.. code:: ipython3

    # Loop over generations
    for igen in range(0, ngen):
        # Update
        swarm.update(control=1)
        # Evaluation
        for indv in range(0, nindv):
            vfit = peaksF(swarm.current[indv, 0, 0], swarm.current[indv, 0, 1])
            if vfit < swarm.misfit[indv]:
                swarm.history[indv, :, :] = swarm.current[indv, :, :]
                swarm.misfit[indv] = vfit
        # Store the misfit values
        fit[igen+1, 0] = np.amin(swarm.misfit)
        fit[igen+1, 1] = np.mean(swarm.misfit)

.. code:: ipython3

    fig = plt.figure(figsize=(10, 4))
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_xlim(-3.0, 3.0)
    ax1.set_ylim(-3.0, 3.0)
    ax1.set_xlabel(r'$x_{1}$')
    ax1.set_ylabel(r'$x_{2}$')
    ax1.imshow(F, aspect='auto', cmap='jet', extent=[-3.0, 3.0, -3.0, 3.0], origin='upper-left')
    ax1.scatter(swarm.history[:, 0, 0], swarm.history[:, 0, 1], color='black')
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_xlabel('Number of generation')
    ax2.set_ylabel('Lower value of peak function found')
    ax2.plot(fit[:, 0], color='red')
    ax2.plot(fit[:, 1], color='gray');



.. image:: images/pso_basics_02.png
