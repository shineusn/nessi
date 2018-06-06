
 Muting SU data
===============

.. code:: ipython3

    # Import matplotlib
    import numpy as np
    import matplotlib.pyplot as plt

    # Import the SUdata class from nessi.io module
    from nessi.io import SUdata

    # Declare
    dobs = SUdata()

    # Read the SU file
    dobs.read('data/musc_F50_01.su')

    # Windowing in time between t=0s and t=0.25s
    # The window method takes into account the 'delrt' SU header keyword
    dobswt = dobs.wind(tmin=0., tmax=0.25)

Mute above and below a line
---------------------------

.. code:: ipython3

    # Define a 2-points line
    xmute = np.zeros(2, dtype=np.float32)
    tmute = np.zeros(2, dtype=np.float32)

    xmute[0] = 0;   tmute[0] = 0.05
    xmute[1] = 120; tmute[1] = 0.17

.. code:: ipython3

    # Mute
    dobsm0 = dobswt.mute(xmute, tmute, ntaper=200, mode=0)
    dobsm1 = dobsm0.mute(xmute, tmute, ntaper=200, mode=1)

.. code:: ipython3

    fig = plt.figure(figsize=(18,5))
    plt.subplot(131)
    dobswt.image(clip=0.05, legend=1)
    plt.subplot(132)
    dobsm0.image(clip=0.05, legend=1)
    plt.subplot(133)
    dobsm1.image(clip=0.05, legend=1)




.. image:: images/muting_SU_data_01.png


Mute above a polygonal line
---------------------------

.. code:: ipython3

    # Define a 3-points line
    xmute = np.zeros(3, dtype=np.float32)
    tmute = np.zeros(3, dtype=np.float32)

    xmute[0] = 0;   tmute[0] = 0.05
    xmute[1] = 50;  tmute[1] = 0.10
    xmute[2] = 70; tmute[2] = 0.25

.. code:: ipython3

    # Mute
    dobsm0b = dobswt.mute(xmute, tmute, ntaper=0, mode=0)

.. code:: ipython3

    fig = plt.figure(figsize=(12,5))
    plt.subplot(121)
    dobswt.image(clip=0.05, legend=1)
    plt.subplot(122)
    dobsm0b.image(clip=0.05, legend=1)



.. image:: images/muting_SU_data_02.png
