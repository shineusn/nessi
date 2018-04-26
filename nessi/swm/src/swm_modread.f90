subroutine modread (fname, n1, n2, v)
  !! subroutine: modread
  !> \brief read an input binary file (single precision).
  !> \param[in] fname name of the input physical parameter file
  !> \param[in] n1 The number of grid points in the first direction (z)
  !> \param[in] n2 The number of grid points in the second direction (x)
  !> \param[out] v single precision array of size (n1, n2) containing
  !> parameter values.
  integer, intent(in) :: n1, n2
  real(4), dimension(n1, n2), intent(out) :: v
  character(len=*), intent(in) :: fname
  
  open(11, file=fname, access='direct', recl=n1*n2*4)
  read(11, rec=1) v
  close(11)
  
end subroutine modread
