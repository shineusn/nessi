
Tapering SU data
================

The ``taper`` method of ``SUdata()`` allows to taper the edge traces of
a data panel to zero with several taper types. It also allows to taper
both in time and space.

Linear taper along the time axis
--------------------------------

The ``linear`` type is the default taper type of the ``taper`` method.

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

    # Apply a windowing in time (for convenience only)
    dobsw = dobs.wind(tmin=0., tmax=0.25)

    # Linear taper along the time axis
    # Tbeg and tend must be in [ms]
    dobswtt = dobsw.taper(tbeg=100., tend=100., type='linear')

.. code:: ipython3

    # Plot original and filtered data
    fig = plt.figure(figsize=(12,5))
    plt.subplot(121)
    dobsw.image(clip=0.05, label2='trace number', label1='time [s]', title='Original SU data', legend=1)
    plt.subplot(122)
    dobswtt.image(clip=0.05, label2='trace number', label1='time [s]', title='Tapered data', legend=1)
    plt.show()



.. image:: images/tapering_SU_data_01.png


Linear taper along trace axis
-----------------------------

.. code:: ipython3

    # Linear taper along the trace axis
    dobswttr = dobsw.taper(tr1=40, tr2=40, type='linear')

.. code:: ipython3

    # Plot original and filtered data
    fig = plt.figure(figsize=(12,5))
    plt.subplot(121)
    dobsw.image(clip=0.05, label2='trace number', label1='time [s]', title='Original SU data', legend=1)
    plt.subplot(122)
    dobswttr.image(clip=0.05, label2='trace number', label1='time [s]', title='Tapered data', legend=1)
    plt.show()



.. image:: images/tapering_SU_data_02.png


Linear taper along time and trace axis
--------------------------------------

.. code:: ipython3

    # Linear taper along the trace axis
    dobswtt2 = dobsw.taper(tr1=40, tr2=40, tbeg=100., tend=100., type='linear')

.. code:: ipython3

    # Plot original and filtered data
    fig = plt.figure(figsize=(12,5))
    plt.subplot(121)
    dobsw.image(clip=0.05, label2='trace number', label1='time [s]', title='Original SU data', legend=1)
    plt.subplot(122)
    dobswtt2.image(clip=0.05, label2='trace number', label1='time [s]', title='Tapered data', legend=1)
    plt.show()



.. image:: images/tapering_SU_data_03.png
