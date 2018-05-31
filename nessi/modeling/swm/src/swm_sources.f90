! -------------------------------------------------------------------
! Filename: swm_sources.f90
!   Author: Damien Pageot
!    Email: nessi.develop@protonmail.com
!
! Copyright (C) 2018 Damien Pageot
! ------------------------------------------------------------------
! subroutine ricker, srcspread
! :copyright:
!     Damien Pageot (nessi.develop@protonmail.com)
! :license:
!     GNU Lesser General Public License, Version 3
!     (https://www.gnu.org/copyleft/lesser.html)
! ------------------------------------------------------------------

subroutine ricker(nt, dt, f0, t0, tsrc)

  integer, intent(in) :: nt
  real(4), intent(in) :: dt, f0, t0
  real(4), dimension(nt), intent(out) :: tsrc

  integer :: it
  real :: sigma, pi, t

  pi = 4.*atan(1.)

  do it=1,nt
     t = float(it-1)*dt-t0
     sigma = (pi*f0*(t))*(pi*f0*(t))
     tsrc(it) = (1.-2.*sigma)*exp(-1.*sigma)
  end do

end subroutine ricker

subroutine srcspread(n1, n2, nsp, xs, zs, h, gsrc, sigma)

  integer, intent(in) :: n1, n2, nsp
  real(4), intent(in) :: xs, zs
  real(4), intent(in) :: h, sigma
  real(4), dimension(n1+2*nsp, n2+2*nsp), intent(out) :: gsrc

  integer :: i1, i2, is1, is2, n1e, n2e
  real :: betasum
  real :: x, z, p1, p2

  n1e = n1+2*nsp
  n2e = n2+2*nsp
  is1 = int(zs/h)+nsp+1
  is2 = int(xs/h)+nsp+1

  gsrc(:, :) = 0.

  betasum = 0.

  if( sigma .le. 0.)then
     gsrc(is1, is2) = 1.
  else
     do i2=nsp+1,n2e-nsp
        x = float(i2-1)*h
        do i1=nsp+1,n1e-nsp
           z = float(i1-1)*h
           p2 = (x-xs)*(x-xs)/(sigma*sigma)
           p1 = (z-zs)*(z-zs)/(sigma*sigma)
           gsrc(i1, i2) = exp(-1.*p1-p2)
           betasum = betasum+exp(-1.*p1-p2)
        end do
     end do

     do i2=1,n2e
        do i1=1,n1e
           gsrc(i1, i2) = gsrc(i1, i2)/betasum
        end do
     end do
  endif

end subroutine srcspread
