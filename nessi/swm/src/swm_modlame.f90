subroutine modlame (n1e, n2e, vpe, vse, roe, mu0, mue, lb0, lbmu)

  integer, intent(in) :: n1e, n2e
  real(4), dimension(n1e, n2e), intent(in) :: vpe, vse, roe
  real(4), dimension(n1e, n2e), intent(out) :: mu0, mue, lb0, lbmu
  
  integer :: i1, i2
  
  mu0(:, :) = vse(:, :)*vse(:, :)*roe(:, :)
  
  do i2=1,n2e-1
     do i1=1, n1e-1
        mue(i1, i2) = 1./((1./4.)* &
             (1./mu0(i1,i2)+ &
             1./mu0(i1+1,i2)+ &
             1./mu0(i1,i2+1)+1./mu0(i1+1,i2+1)))
     end do
  end do
  
  mue(:,n2e) = mue(:,n2e-1)
  mue(n1e,:) = mue(n1e-1,:)
  
  lb0(:, :) = vpe(:, :)*vpe(:, :)*roe(:, :) &
       -2.*mu0(:, :)
  
  lbmu(:,:) = lb0(:, :)+2.*mu0(:,:)
  
end subroutine modlame
