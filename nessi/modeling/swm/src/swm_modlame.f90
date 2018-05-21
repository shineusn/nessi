! -------------------------------------------------------------------
! Filename: swm_modlame.f90
!   Author: Damien Pageot
!    Email: nessi.develop@protonmail.com
!
! Copyright (C) 2018 Damien Pageot
! ------------------------------------------------------------------
! subroutine modlame
! :copyright:
!     Damien Pageot (nessi.develop@protonmail.com)
! :license:
!     GNU Lesser General Public License, Version 3
!     (https://www.gnu.org/copyleft/lesser.html)
! ------------------------------------------------------------------

subroutine modlame (n1e, n2e, vpe, vse, roe, mu, lbd, lbdmu)
    !! subroutine: modlame
    !> \brief calculate the Lame models according to the staggered-grid.
    !> \param[in] n1e The number of grid points in the first direction (z)
    !> \param[in] n2e The number of grid points in the second direction (x)
    !> \param[in] vpe Extended P-wave velocity model of size (n1e, n2e)
    !> \param[in] vse Extended S-wave velocity model of size (n1e, n2e)
    !> \param[in] roe Extended density model of size (n1e, n2e)
    !> \param[out] mu Extended shear modulus of size (n1e, n2e)
    !> \param[out] lbd Extended Lame modulus of size (n1e, n2e)
    !> \param[out] lbdmu Extended lbd+2mu of size (n1e, n2e)

    integer, intent(in) :: n1e, n2e
    real(4), dimension(n1e, n2e), intent(in) :: vpe, vse, roe
    real(4), dimension(n1e, n2e), intent(out) :: mu, lbd, lbdmu

    integer :: i1, i2
    real(4), dimension(n1e, n2e) :: mu0

    mu0(:, :) = vse(:, :)*vse(:, :)*roe(:, :)

    do i2=1,n2e-1
        do i1=1, n1e-1
            mu(i1, i2) = 1./((1./4.)*(1./mu0(i1,i2)+ &
                1./mu0(i1+1,i2)+1./mu0(i1,i2+1)+1./mu0(i1+1,i2+1)))
        end do
    end do

    mu(:,n2e) = mu(:,n2e-1)
    mu(n1e,:) = mu(n1e-1,:)

    lbd(:, :) = vpe(:, :)*vpe(:, :)*roe(:, :)-2.*mu0(:, :)
    lbdmu(:,:) = lbd(:, :)+2.*mu0(:,:)

end subroutine modlame
