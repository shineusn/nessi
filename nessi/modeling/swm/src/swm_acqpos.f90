subroutine acqpos(n1, n2, npml, dh, nrec, acq, recpos)
  integer, intent(in) :: n1, n2, npml, nrec
  real(4), intent(in) :: dh
  real(4), dimension(nrec, 2), intent(in) :: acq
  integer, dimension(nrec, 2), intent(out) :: recpos

  integer :: irec
  real(4) :: xmax, zmax, lpml

  xmax = float(n2+2*npml-1)*dh
  zmax = float(n1+2*npml-1)*dh
  lpml = float(npml)*dh
  
  do irec=1,nrec
     recpos(irec, 1) = int((acq(irec, 1)+lpml)/dh)+1
     recpos(irec, 2) = int((acq(irec, 2)+lpml)/dh)+1
  end do

end subroutine acqpos
