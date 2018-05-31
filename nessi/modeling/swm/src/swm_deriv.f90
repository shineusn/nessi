! -------------------------------------------------------------------
! Filename: swm_deriv.f90
!   Author: Damien Pageot
!    Email: nessi.develop@protonmail.com
!
! Copyright (C) 2018 Damien Pageot
! ------------------------------------------------------------------
! subroutines dxforward, dxbackward, dzforward, dzbackward
! :copyright:
!     Damien Pageot (nessi.develop@protonmail.com)
! :license:
!     GNU Lesser General Public License, Version 3
!     (https://www.gnu.org/copyleft/lesser.html)
! ------------------------------------------------------------------

subroutine dxforward(f, n1, n2, d)
  !> \brief 4th order forward derivative in the x-direction.\n
  !> \f$ D^{+}_{x} = c1*[f(i,j+1)-f(i,j)]+c2*[f(i,j+2)-f(i,j-1)]\f$.
  !> \param[out] d  derivative
  !> \param[in]  f  array of size n1*n2 to derive
  !> \param[in]  n1 The number of grid points in the first direction (z)
  !> \param[in]  n2 The number of grid points in the second direction (x)
  integer :: i2
  real, parameter :: c1=(9./8.), c2=(-1./24.)
  integer, intent(in) :: n1, n2
  real(4), dimension(n1,n2), intent(in) :: f
  real(4), dimension(n1,n2), intent(out) :: d

  d(:, : ) = 0.

  !! >> 4th order derivative
  !$OMP PARALLEL DO SHARED(n2, d, f)
  do i2=2,n2-2
     d(:,i2) = c1*(f(:,i2+1)-f(:,i2))+c2*(f(:,i2+2)-f(:,i2-1))
  end do
  !$OMP END PARALLEL DO

  !! >> 2nd order derivative
  d(:,1) = f(:,2)-f(:,1)
  d(:,n2-1) = f(:,n2)-f(:,n2-1)

end subroutine dxforward

subroutine dxbackward(f, n1, n2, d)
  !> @brief 4th order backward derivative in the x-direction.\n
  !> \f$ D^{-}_{x} = c1*[f(i,j)-f(i,j-1)]+c2*[f(i,j+1)-f(i,j-2)]\f$.
  !> @param[out] d  derivative
  !> @param[in]  f  array of size n1*n2 to derive
  !> @param[in]  n1 The number of grid points in the first direction (z)
  !> @param[in]  n2 The number of grid points in the second direction (x)
  integer :: i2

  real, parameter :: c1=(9./8.), c2=(-1./24.)
  integer, intent(in) :: n1, n2
  real(4), dimension(n1,n2), intent(in) :: f
  real(4), dimension(n1,n2), intent(out) :: d

  d(:, : ) = 0.

  !! >> 4th order derivative
  !$OMP PARALLEL DO SHARED(n2, d, f)
  do i2=3,n2-1
     d(:,i2) = c1*(f(:,i2)-f(:,i2-1))+c2*(f(:,i2+1)-f(:,i2-2))
  end do
  !$OMP END PARALLEL DO

  !! >> 2nd order derivative
  d(:,2) = f(:,2)-f(:,1)
  d(:,n2) = f(:,n2)-f(:,n2-1)

end subroutine dxbackward

subroutine dzforward(f, n1, n2, nsp, d, isurf)
  !> @brief 4th order forward derivative in the z-direction.\n
  !> \f$ D^{+}_{z} = c1*[f(i+1,j)-f(i,j)]+c2*[f(i+2,j)-f(i-1,j)]\f$.
  !> @param[out] d  derivative
  !> @param[in]  f  array of size n1*n2 to derive
  !> @param[in]  n1 The number of grid points in the first direction (z)
  !> @param[in]  n2 The number of grid points in the second direction (x)
  integer :: i1, i1beg

  real, parameter :: c1=(9./8.), c2=(-1./24.)
  integer, intent(in) :: n1, n2, nsp, isurf
  real(4), dimension(n1,n2), intent(in) :: f
  real(4), dimension(n1,n2), intent(out) :: d

  d(:, : ) = 0.

  if( isurf == 1)then
     i1beg = nsp+2 !!!
  else
     i1beg = 2
  endif

  !! >> 4th order derivative
  !$OMP PARALLEL DO SHARED(n1, d, f)
  do i1=i1beg,n1-2
     d(i1,:) = c1*(f(i1+1,:)-f(i1,:))+c2*(f(i1+2,:)-f(i1-1,:))
  end do
  !$OMP END PARALLEL DO

  !! >> 2nd order derivative
  if(isurf == 1)then
     i1beg = nsp+1
  else
     i1beg = 1
  endif

  d(i1beg,:) = f(i1beg+1,:)-f(i1beg,:)
  d(n1-1,:) = f(n1,:)-f(n1-1,:)

end subroutine dzforward

subroutine dzbackward(f, n1, n2, nsp, d, isurf)
  !> @brief 4th order backward derivative in the z-direction.\n
  !> \f$ D^{-}_{z} = c1*[f(i,j)-f(i-1,j)]+c2*[f(i+1,j)-f(i-2,j)]\f$.
  !> @param[out] d  derivative
  !> @param[in]  f  array of size n1*n2 to derive
  !> @param[in]  n1 The number of grid points in the first direction (z)
  !> @param[in]  n2 The number of grid points in the second direction (x)
  integer :: i1, i1beg

  real, parameter :: c1=(9./8.), c2=(-1./24.)
  integer, intent(in) :: n1, n2, nsp, isurf
  real(4), dimension(n1,n2), intent(in) :: f
  real(4), dimension(n1,n2), intent(out) :: d

  d(:, : ) = 0.

  if(isurf == 1)then
     i1beg = nsp+2
  else
     i1beg = 3
  endif

  !! >> 4th order derivative
  !$OMP PARALLEL DO SHARED(n1, d, f)
  do i1=i1beg,n1-1
     d(i1,:) = c1*(f(i1,:)-f(i1-1,:))+c2*(f(i1+1,:)-f(i1-2,:))
  end do
  !$OMP END PARALLEL DO

  if(isurf == 1)then
     i1beg = nsp+1
  else
     i1beg = 2
  endif

  !! >> 2nd order derivative
  d(i1beg,:) = f(i1beg,:)-f(i1beg-1,:)
  d(n1,:) = f(n1,:)-f(n1-1,:)

end subroutine dzbackward
