
Filtering SU data
=================

The ``pfilter`` method of ``SUdata()`` allows to apply a zero-phase,
sine-squared tapered filter to the data.

Sine-squared taper
------------------

.. code:: ipython3

    # Import numpy and matplotlib
    import numpy as np
    import matplotlib.pyplot as plt

    # Import the SUdata class from nessi.io module
    from nessi.io import SUdata

    # Declare
    dobs = SUdata()

    # Read the SU file
    dobs.read('data/musc_F50_01.su')

    # Create frequency and amplitude arrays for filtering
    freq = np.zeros(4, dtype=np.float32)
    amps = np.zeros(4, dtype=np.float32)

    freq[0] = 10.; freq[1] = 100.; freq[2] = 250.; freq[3] = 300.;
    amps[0] = 0.;  amps[1] = 1.0; amps[2] = 1.0;  amps[3] = 0.0;

    # Filtering
    dobsf = dobs.pfilter(freq, amps)

.. code:: ipython3

    # Plot original and filtered data
    fig = plt.figure(figsize=(12,5))
    plt.subplot(121)
    dobs.image(clip=0.05, label2='trace number', label1='time [s]', title='Original SU data', legend=1)
    plt.subplot(122)
    dobsf.image(clip=0.05, label2='trace number', label1='time [s]', title='Filtered data', legend=1)
    plt.show()



.. image:: images/filtering_SU_data_01.png
