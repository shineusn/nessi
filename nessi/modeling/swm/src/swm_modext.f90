! -------------------------------------------------------------------
! Filename: swm_modext.f90
!   Author: Damien Pageot
!    Email: nessi.develop@protonmail.com
!
! Copyright (C) 2018 Damien Pageot
! ------------------------------------------------------------------
! subroutine modext
! :copyright:
!     Damien Pageot (nessi.develop@protonmail.com)
! :license:
!     GNU Lesser General Public License, Version 3
!     (https://www.gnu.org/copyleft/lesser.html)
! ------------------------------------------------------------------

subroutine modext(n1, n2, npml, v, ve)
    !! subroutine: modext
    !> \brief extend parameter model with absording boundary condition.
    !> \param[in] n1 The number of grid points in the first direction (z)
    !> \param[in] n2 The number of grid points in the second direction (x)
    !> \param[in] npml The number of grid points added for ABC layers
    !> \param[in] v physical parameter array of size (n1, n2)
    !> \param[out] ve physical parameter array of size (n1+2*npml, n2+2*npml)

    integer, intent(in) :: n1, n2, npml
    real(4), dimension(n1, n2), intent(in) :: v
    real(4), dimension(n1+2*npml, n2+2*npml), intent(out) :: ve

    !# Fill the extended model with the original one
    ve(npml+1:n1+npml, npml+1:n2+npml) = v(1:n1, 1:n2)

    !# Fill the model extensions with boundary values
    do i=1,npml
        ve(:, i) = ve(:, npml+1)
        ve(:, n2+npml+i) = ve(:, n2+npml)
    end do

    !# Fill the model extensions with boundary values
    do i=1,npml
        ve(i, :) = ve(npml+1, :)
        ve(n1+npml+i, :) = ve(n1+npml, :)
    end do

end subroutine modext