subroutine modext(n1, n2, nsp, v, ve)
  !! subroutine: modext
  !> \brief extend parameter model with absording boundary condition
  !> (ABC) layers.
  !> \param[in] v physical parameter array of size (n1, n2)
  !> \param[in] n1 The number of grid points in the first direction (z)
  !> \param[in] n2 The number of grid points in the second direction (x)
  !> \param[in] nsp The number of grid points added for ABC layers 
  !> \param[out] ve physical parameter array of size (n1+2*nsp, n2+2*nsp)
  integer :: i
  integer, intent(in) :: n1, n2, nsp
  real(4), dimension(n1+2*nsp,n2+2*nsp), intent(out) :: ve
  real(4), dimension(n1,n2), intent(in) :: v
  
  !f2py integer intent(in) :: n1, n2, nsp
  !f2py real(4) intent(in) :: v
  !f2py real(4) intent(out) :: ve
  
  ve(nsp+1:n1+nsp,nsp+1:n2+nsp) = v(1:n1,1:n2)
  
  do i=1,nsp
     ve(:,i) = ve(:,nsp+1)
     ve(:,n2+nsp+i) = ve(:,n2+nsp)
  end do
  
  do i=1,nsp
     ve(i, :) = ve(nsp+1, :)
     ve(n1+nsp+i, :) = ve(n1+nsp, :)
  end do
  
end subroutine modext
