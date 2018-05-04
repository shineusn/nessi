! -------------------------------------------------------------------
! Filename: swm_modbuo.f90
!   Author: Damien Pageot
!    Email: nessi.develop@protonmail.com
!
! Copyright (C) 2018 Damien Pageot
! ------------------------------------------------------------------
! subroutine modbuo
! :copyright:
!     Damien Pageot (nessi.develop@protonmail.com)
! :license:
!     GNU Lesser General Public License, Version 3
!     (https://www.gnu.org/copyleft/lesser.html)
! ------------------------------------------------------------------

subroutine modbuo (n1e, n2e, roe, bux, buz)
    !! subroutine: modbuo
    !> \brief calculate the buoyancy models (bux and buz).
    !> \param[in] n1e The number of grid points in the first direction (z)
    !> \param[in] n2e The number of grid points in the second direction (x)
    !> \param[in] roe Extended density model of size (n1e, n2e)
    !> \param[out] bux Extended buoyancy of size (n1+2*npml, n2+2*npml)
    !> \param[out] bux Extended buoyancy of size (n1+2*npml, n2+2*npml)

    integer, intent(in) :: n1e, n2e
    real(4), intent(in), dimension(n1e, n2e) :: roe
    real(4), intent(out), dimension(n1e, n2e) :: bux
    real(4), intent(out), dimension(n1e, n2e) :: buz

    integer :: i1, i2

    !# Calculate bux
    do i2=1,n2e-1
        bux(:, i2) = (1./2.)*(1./roe(:, i2)+1./roe(:, i2+1))
    end do
    bux(:,n2e) = 1./roe(:,n2e)

    !# Calculate buz
    do i1=1,n1e-1
        buz(i1, :) = (1./2.)*(1./roe(i1, :)+1./roe(i1+1, :))
    end do
    buz(n1e,:) = 1./roe(n1e,:)

end subroutine modbuo
