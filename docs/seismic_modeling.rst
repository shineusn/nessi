***************************
2D elastic seismic modeling
***************************

============
Introduction
============

In order to solve the wave motion equation, a variety of numerical method have been developed such as the finite-differences method (:cite:`kelly1976synthetic,virieux1984sh,virieux1986psv,li2016optimal`), the pseudo-spectral method (:cite:`faccioli19972d`), the finite-element method (:cite:`seron1990finite,mahmoudian2003review`) or the spectral element method (:cite:`komatitsch1999spectral,komatitsch2005spectral`). Among these methods, the finite-difference method (FD) is the most popular and one of the most widely used because of its ease of implementation and use, its robustness, and its reasonable computational cost.

==================
Governing equation
==================

The equation of motion in an elastic medium can be written, in its compact formulation, as (:cite:`aki2002quantitative,virieux2016modelling`):

.. math:: \rho(\mathbf{x}) \frac{\partial^{2}\mathbf{u}_{i}}{\partial t^{2}} = \frac{\partial \mathbf{\sigma}_{ik}}{\partial \mathbf{x}_{k}} + \rho(\mathbf{x})f_{i},
	  :label: motion
	   
where :math:`\mathbf{x}=(x,y,z)` is the position vector, :math:`\mathbf{u}` is the displacement field, :math:`\mathbf{\sigma}_{ij}` is the stress tensor, :math:`\rho(\mathbf{x})` is the density and :math:`f=(f_{x}, f_{y}, f_{z})` is the a volumetric force.

The stress tensor :math:`\sigma`, which allows to describe the elastic medium, is lineary relied to the strain tensor :math:`\epsilon` through the fourth-rank elastic tensor :math:`C_{ijkl}`. This linear relation, called generalized Hooke's law,  is defined as follow:

.. math:: \sigma_{ij} = C_{ijkl}\epsilon_{kl}\ ,
	  :label: hooke

where

.. math:: C_{ijkl} = \lambda \delta_{ij} \delta_{kl} + \mu (\delta_{ik}\delta_{jl}+\delta_{il}\delta_{jk})\ ,
	  :label: elastic-tensor

where :math:`\delta` is the Kronehker symbol and :math:`\lambda` and :math:`\mu` are the Lamé parameters.

The strain tensor corresponds to the symetric part of the displacement derivatives with respect to space, *i.e.* to the deformation of the elastic body such as:

.. math:: \epsilon_{ij} = \frac{1}{2} \left( \frac{\partial u_{j}}{\partial x_{i}} + \frac{\partial u_{i}}{\partial x_{j}} \right)\ .
	  :label: strain-tensor

Combining equations :eq:`hooke` and :eq:`strain-tensor`, and injecting the result in equation :eq:`motion` leads to the second order hyperbolic system, called displacement-stress formulation. In 2D, where all derivative with respect to :math:`y` vanishes, the displacement-stress formulation is:

.. math::
   \frac{\partial ^{2} u_{x}}{\partial t^{2}} = \rho^{{\scriptscriptstyle-1}} \left( \frac{\partial \sigma_{xx}}{\partial x} + \frac{\partial \sigma_{xz}}{\partial z} \right)\ , \nonumber \\
  \frac{\partial ^{2} u_{z}}{\partial t^{2}} = \rho^{{\scriptscriptstyle -1}} \left( \frac{\partial \sigma_{xz}}{\partial x} + \frac{\partial \sigma_{zz}}{\partial z} \right)\ ,
  :label: displacement-stress

where:

.. math::
   \sigma_{xx} = (\lambda+2\mu)\frac{\partial u_{x}}{\partial x} + \lambda \frac{\partial u_{z}}{\partial z}\ , \nonumber \\
  \sigma_{zz}= (\lambda+2\mu)\frac{\partial u_{z}}{\partial z} + \lambda \frac{\partial u_{x}}{\partial x}\ , \\
  \sigma_{xz} = \mu \left( \frac{\partial u_{x}}{\partial z} + \frac{\partial u_{z}}{\partial x } \right)\ . \nonumber
  :label: displacement-stress2

This system can be expressed in term of velocity instead of displacement which leads to the first-order hyperbolic system, called velocity-stress formulation:

.. math::
     \frac{\partial v_{x}}{\partial t} = \rho^{{\scriptscriptstyle-1}} \left( \frac{\partial \sigma_{xx}}{\partial x} + \frac{\partial \sigma_{xz}}{\partial z} \right) \nonumber \\
     \frac{\partial v_{z}}{\partial t} = \rho^{{\scriptscriptstyle -1}} \left( \frac{\partial \sigma_{xz}}{\partial x} + \frac{\partial \sigma_{zz}}{\partial z} \right) \nonumber \\
     \frac{\partial \sigma_{xx}}{\partial t} = (\lambda+2\mu)\frac{\partial v_{x}}{\partial x} + \lambda \frac{\partial v_{z}}{\partial z} \\
     \frac{\partial \sigma_{zz}}{\partial t} = (\lambda+2\mu)\frac{\partial v_{z}}{\partial z} + \lambda \frac{\partial v_{x}}{\partial x} \nonumber \\
     \frac{\partial \sigma_{xz}}{\partial t} = \mu \left( \frac{\partial v_{x}}{\partial z} + \frac{\partial v_{z}}{\partial x } \right) \nonumber
     :label: velocity-stress

==============
Staggered grid
==============

The staggered-grid approach (:cite:`levander1988fourth`), initially developed for two-dimensional P-Sv seismic wave propagation modeling, is fourth-order accurate space and second order accurate time (:math:`O(\Delta t^{2},h^{4})`) numerical scheme.

The staggered-grid allows to correctly model any variation of the material properties with a minimal numerical dispersion and anisotropy. The scheme can also be used to model wave propagation in mixed acoustic-elastic media with a good accuracy.

:cite:`virieux1986psv,bohlen2006accuracy`

.. figure:: images/fdtd/staggered.png
	    :figwidth: 90 %
	    :align: center

	    Staggered finite-difference grid and spatial stencils for (a) the velocity update and (b) the stress update. After :cite:`levander1988fourth` with velocity-stress position switch proposed by :cite:`bohlen2006accuracy`.

==============
Discretization
==============

Given the use of the staggered-grid scheme to discretize the space, forward and backward finite-difference operators are use to solve the velocity-stress equations.

The fourth-order forward (:math:`D^{+}`) and backward (:math:`D^{-}`) operators are widely used and are defined, in 1D, as:

.. math::
   D^{+}=c_{1}[f(i+1)-f(i)]+c_{2}[f(i+2)-f(i-1)] \nonumber \\
   D^{-}=c_{1}[f(i)-f(i-1)]+c_{2}[f(i+1)-f(i-2)]
   :label: fd-forward-backward

:cite:`graves1996simulating`

.. math::
   \bar{\mu}(i+\frac{1}{2}, j+\frac{1}{2})=\left[ \frac{1}{4} \left( \frac{1}{\mu(i,j)}+\frac{1}{\mu(i+1,j)}+\frac{1}{\mu(i,j+1)}+\frac{1}{\mu(i+1,j+1)} \right) \right]^{-1} \\
  \rho_{x}(i,j+\frac{1}{2}) = \frac{1}{2}(\rho (i,j+1)+\rho(i,j)) \\
  \rho_{z}(i+\frac{1}{2},j) = \frac{1}{2}(\rho (i+1,j)+\rho(i,j))

===============================
Initial and boundary conditions
===============================

---------------------------------
PML absorbing boundary conditions
---------------------------------

At the scale of seismic exploration and less, the target area (*i.e.* the model), is a semi-infinite space bounded only at the top by a free surface. It is thus necessary to simulate a infinite medium at the lateral and bottom boundary. This can be achieve using the *Perfectly Matched Layer* (PML) absorbing boundaries. PML were initially developed in the framework of electro-magentic modeling by :cite:`berenger1994perfectly` and was quickly adopted in seismic modeling.

In the time domain, PML can be defined as:

.. math:: d = d_{0} \left( \frac{q}{L_{PML}} \right) ^{n}\ , \\
	  d_{0} = Ac_{p} \frac{log(1/R)}{2L_{PML}}\ ,
	  :label: pml
		  
where :math:`q` is the distance from PML intern boundary, :math:`L_{PML}` is the width of the PML, :math:`A` is the amplitude of the PML, :math:`c_{p}` is the P-wave velocity and :math:`R` is a reflection coefficient generally low. PML are parametrized following recommandations of :cite:`festa2005newmark`: :math:`A=3` and :math:`R=0.01`.

------------
Free surface
------------

As discussed in the previous subsection, the earth structures must be considered as semi-infinite space due to the presence of a free surface defined by the topography. Given the strong formulation of the wave equation used by finite-difference methods, the free surface must be explicitly defined.

The image theory method is a way to apprximate the free surface and was firstly proposed by :cite:`levander1988fourth`.

At free surface boundary condition :math:`z=0`, all normal stresses vanish:

.. math:: \sigma_{zz} = \lambda \frac{\partial u_{x}}{\partial x}+(\lambda+2\mu)\frac{\partial u_{z}}{\partial z} =0 \nonumber \\
	  \sigma_{xz} = \mu \left( \frac{\partial u_{z}}{\partial x} + \frac{\partial u_{x}}{\partial z} \right) = 0
	  
If the free surface on the staggered grid is defined along :math:`\sigma_{zz}`, :math:`\sigma_{zz}` is explicitly set to 0 and :math:`\sigma_{xz}` over the free surface is an odd function such as:

.. math:: \sigma_{zz}^{z(i)=0}(i,j) = 0, \nonumber \\
	  \sigma_{zz}^{z(i)=0}(i-\frac{1}{2},j) = -\sigma_{zz}^{z(i)=0}(i+\frac{1}{2},j)

	  
---------------------	  
Fluid-solid interface
---------------------

Given the use of harmonic averaging of :math:`\mu`, at the fluid-solid interface :math:`\tau_{xz}` naturally vanishes and satisfies implicitly the continuity conditions through the fluid-solid interface (:cite:`vanvossen2002finite`).

=======
Sources
=======

----------------
Explosive source
----------------

Explosive source is added to normal stress :math:`\sigma_{xx}` and :math:`\sigma{zz}`.

.. math:: F(i,j,t) = S(t)\frac{\Delta t}{\Delta x^{2}}

-----------------	  
Body force source
-----------------

------------
Source types
------------

=======================
Precision and stability
=======================

==========
References
==========

.. bibliography:: references.bib
