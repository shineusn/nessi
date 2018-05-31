! -------------------------------------------------------------------
! Filename: swm_pmlmod.f90
!   Author: Damien Pageot
!    Email: nessi.develop@protonmail.com
!
! Copyright (C) 2018 Damien Pageot
! ------------------------------------------------------------------
! subroutines pmlmod, dirichlet
! :copyright:
!     Damien Pageot (nessi.develop@protonmail.com)
! :license:
!     GNU Lesser General Public License, Version 3
!     (https://www.gnu.org/copyleft/lesser.html)
! ------------------------------------------------------------------

subroutine pmlmod (n1, n2, h, isurf, npml, apml, ppml, pmlx0, pmlx1, pmlz0, pmlz1)

  integer, intent(in) :: n1, n2, npml, ppml, isurf
  real(4), intent(in) :: h, apml
  real(4), dimension(n1+2*npml, n2+2*npml), intent(out) :: pmlx0, pmlx1
  real(4), dimension(n1+2*npml, n2+2*npml), intent(out) :: pmlz0, pmlz1

  ! ADD IF ISURF HERE
  ! DO NOT CONSTRUCT TOP PML IN CASE OF FREE SURFACE.
  integer :: i, n1e, n2e
  real :: val0, val1, val2

  real :: r, d0, l

  n1e = n1+2*npml
  n2e = n2+2*npml
  ! >> Initialize pml arrays
  pmlx0(:, :) = 0.
  pmlx1(:, :) = 0.
  pmlz0(:, :) = 0.
  pmlz1(:, :) = 0.

  r = 0.0001 !0.9
  !vpmax = maxval(vpe)
  l = float(npml-1)*h
  !d0 = tbnd%apml*vpmax*log(1./r)/(2*l)
  d0 = float(ppml+1)*apml*log(1./r)/(2.*l)

  do i=1,npml+1
     val0 = float(npml-i+1)*h
     val1 = float(npml-i+1)*h-(h/2.)
     val2 = float(npml-i+1)*h+(h/2.)
     if (isurf == 1) then
        pmlz0(i, :) = 0. !d0*(val0/l)**2
        pmlz1(i, :) = 0. !d0*(val1/l)**2
     else
        pmlz0(i, :) = d0*(val0/l)**ppml !2
        pmlz1(i, :) = d0*(val1/l)**ppml !2
     endif
     !tbnd%pmlz0(i, :) = d0*(val0/l)**ppml
     !tbnd%pmlz1(i, :) = d0*(val1/l)**ppml
     pmlz0(n1e+1-i,:) = d0*(val0/l)**ppml
     pmlz1(n1e+1-i, :) = d0*(val2/l)**ppml
     pmlx0(:, i) = d0*(val0/l)**ppml !2 !ppml
     pmlx0(:, n2e+1-i) = d0*(val0/l)**ppml
     pmlx1(:, i) = d0*(val1/l)**ppml !2 !ppml
     pmlx1(:, n2e+1-i) = d0*(val2/l)**ppml
  enddo

  pmlx0(:, :) = pmlx0(:, :)/2.
  pmlx1(:, :) = pmlx1(:, :)/2.
  pmlz0(:, :) = pmlz0(:, :)/2.
  pmlz1(:, :) = pmlz1(:, :)/2.

end subroutine pmlmod


subroutine dirichlet(n1e, n2e, uxx, uxz, uzx, uzz)
  ! implement Dirichlet boundary conditions on the four edges of the grid
  integer, intent(in) :: n1e, n2e
  real(4), dimension(n1e,n2e), intent(inout) :: uxx, uxz, uzx, uzz

  uxx(1, :) = 0.
  uxx(n1e, :)= 0.
  uxx(:, 1) = 0.
  uxx(:, n2e)= 0.

  uxz(1, :) = 0.
  uxz(n1e, :)= 0.
  uxz(:, 1) = 0.
  uxz(:, n2e)= 0.

  uzx(1, :) = 0.
  uzx(n1e, :)= 0.
  uzx(:, 1) = 0.
  uzx(:, n2e)= 0.

  uzz(1, :) = 0.
  uzz(n1e, :)= 0.
  uzz(:, 1) = 0.
  uzz(:, n2e)= 0.

end subroutine dirichlet
