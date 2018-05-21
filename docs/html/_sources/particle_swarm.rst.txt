***************************
Particle Swarm Optimization
***************************

============
Introduction
============

Particle swarm optimization (PSO), first proposed by :cite:`eberhart1995new`, is a population-based algorithm which intends for simulating the social behavior of a bird flock (swarm of particles) to reach the optimum region of the search space.

PSO is quite recent in the framework of geophysical data inversion (:cite:`shaw2007particle,yuan2009swarm`) and is not yet widely used like well-known global optimization methods such as Monte-Carlo (:cite:`metropolis1949monte,mosegaard1995monte,mosegaard2002monte,socco2008improved`), simulated-annealing (:cite:`ryden2006fast`) or neighbourhood algorithm (:cite:`sambridge1999neighbourhood,sambridge1999neighbourhoodb,sambridge2001finding`). However, it was successfully applied to surface-wave analysis (:cite:`song2012application,wilken2012application`), traveltime tomography (:cite:`tronicke2012crosshole,luu2016competitive`), seismic refraction (:cite:`poormirzaee2014introducing`) and seismic wave impedance inversion in igneous rock (:cite:`yang2017particle`).

(:cite:`banks2007review,banks2008review,zhang2015comprehensive`).


======
Method
======

In PSO, individuals *i*, or particles, are characterized by a velocity vector :math:`\mathbf{V}_{i}=[v_{i}^{1},...,v_{i}^{d},...,v_{i}^{D}]\ \in \mathrm{R}^{D}` and a position vector :math:`\mathbf{X}_{i}=[x_{i}^{1},...,x_{i}^{d},...,x_{i}^{D}]\ \in \mathrm{R}^{D}` in D-dimensional solution space. All particles are initialized with random values at the beginning of the inversion process and the corresponding velocity vectors are set to zero.

The standard PSO update formulas are (:cite:`eberhart1995new`):

.. math:: \mathbf{V}_{i}^{k} = \mathbf{V}_{i}^{k-1}+c_{p} \times \mathbf{r_{p}} \times (\mathbf{X}_{\mathbf{p},i}-\mathbf{X}_{i}^{k-1})+c_{g} \times \mathbf{r_{g}} \times (\mathbf{X}_{\mathbf{g}}-\mathbf{X}_{i}^{k-1})
	  :label: pso_canonical_update_v

.. math:: \mathbf{X}_{i}^{k} = \mathbf{X}_{i}^{k-1}+ \mathbf{V}_{i}^{k}\ ,
	  :label: pso_canonical_update_x

where :math:`\mathbf{r_{p}}` and :math:`\mathbf{r_{2}}` are vectors of random values that induce stochacity (:cite:`souravlias2016particle`), :math:`c_{p}` is the cognitive parameter, :math:`c_{g}` is the social parameter and :math:`c_{p}=c_{g}=2` in most cases.

Classical improvements of PSO concern the control of the velocity vector through the use of an inertia weight :math:`w` (:cite:`bansal2011inertia`) or a constriction factor :math:`\chi` (:cite:`shi1998modified,clerc1999swarm,eberhart2000comparing`).

.. math:: \mathbf{V}_{i}^{k} = w \times \mathbf{V}_{i}^{k-1}+c_{p} \times \mathbf{r_{p}} \times (\mathbf{X}_{\mathbf{p},i}-\mathbf{X}_{i}^{k-1})+c_{g} \times \mathbf{r_{g}} \times (\mathbf{X}_{\mathbf{g}}-\mathbf{X}_{i}^{k-1})\ ,
	  :label: inertia_update

.. math:: \mathbf{V}_{i}^{k} = \chi \times \left[ \mathbf{V}_{i}^{k-1}+c_{p} \times \mathbf{r_{p}} \times (\mathbf{X}_{\mathbf{p},i}-\mathbf{X}_{i}^{k-1})+c_{g} \times \mathbf{r_{g}} \times (\mathbf{X}_{\mathbf{g}}-\mathbf{X}_{i}^{k-1}) \right]\ .
	  :label: constriction_update

Note that the value of :math:`\chi` is directly related to the values of :math:`c_{p}` and :math:`c_{g}` such as:

.. math:: \chi = \frac{2}{2-\phi-\sqrt{\phi^{2}-4\phi}}\ , . 
	  :label: constriction_factor

where :math:`\phi=c_{p}+c_{g}` and :math:`\phi > 4.1`. For :math:`c_{p}=c_{g}=2.05`, equation :eq:`constriction_update` is equivalent to equation :eq:`inertia_update` using :math:`\omega= 0.7298` and :math:`c_{p}=c_{g}=1.4962`.

.. code-block:: console
		
		Add pseudo-code image here

==========
References
==========

.. bibliography:: references.bib
