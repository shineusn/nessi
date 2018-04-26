subroutine modbuo (n1e, n2e, roe, bux, buz)
  
  integer, intent(in) :: n1e, n2e
  real(4), intent(in), dimension(n1e, n2e) :: roe
  real(4), intent(out), dimension(n1e, n2e) :: bux
  real(4), intent(out), dimension(n1e, n2e) :: buz
  
  integer :: i1, i2
  
  do i2=1,n2e-1
     bux(:, i2) = (1./2.)*(1./roe(:, i2)+1./roe(:, i2+1))
  end do
  bux(:,n2e) = 1./roe(:,n2e)
  
  do i1=1,n1e-1
     buz(i1, :) = (1./2.)*(1./roe(i1, :)+1./roe(i1+1, :))
  end do
  buz(n1e,:) = 1./roe(n1e,:)
  
end subroutine modbuo
