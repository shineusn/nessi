! -------------------------------------------------------------------
! Filename: swm_marching.f90
!   Author: Damien Pageot
!    Email: nessi.develop@protonmail.com
!
! Copyright (C) 2018 Damien Pageot
! ------------------------------------------------------------------
! subroutine marching
! :copyright:
!     Damien Pageot (nessi.develop@protonmail.com)
! :license:
!     GNU Lesser General Public License, Version 3
!     (https://www.gnu.org/copyleft/lesser.html)
! ------------------------------------------------------------------

subroutine evolution(n1, n2, h, npml, nt, nts, ntsnap, dt, nrec, srctype, &
     tsrc, gsrc, recx, recz, recp, recpos, isurf, isnap, bux, buz, lb0, lbmu, mue, &
     pmlx0, pmlx1, pmlz0, pmlz1)

  implicit none

  integer, intent(in) :: n1, n2, npml
  integer, intent(in) :: nt, nts, ntsnap, nrec, srctype
  integer, intent(in) :: isurf, isnap
  real(4), intent(in) :: dt, h

  real(4), dimension(nt), intent(in) :: tsrc
  real(4), dimension(n1+2*npml,n2+2*npml), intent(in) :: gsrc
  real(4), dimension(n1+2*npml, n2+2*npml), intent(in) :: pmlx0, pmlx1, pmlz0, pmlz1

  integer, dimension(nrec,2), intent(in) :: recpos

  real(4), dimension(nts, nrec), intent(out) :: recx, recz, recp
  real(4), dimension(n1+2*npml, n2+2*npml), intent(in) :: bux, buz, lb0, lbmu, mue


  integer :: i1, i2, it, its, ets, itsnap, n1e, n2e
  integer :: etsnap, ix, iz, irec, itt
  real :: start, finish
  real :: full
  real :: dth

  real, allocatable :: ux(:, :), uz(:, :), txx(:, :), tzz(:, :), txz(:, :)
  real, allocatable :: uxx(:, :), uxz(:, :)
  real, allocatable :: uzx(:, :), uzz(:, :)
  real, allocatable :: txxx(:, :), txxz(:, :)
  real, allocatable :: tzzx(:, :), tzzz(:, :)
  real, allocatable :: txzx(:, :), txzz(:, :)

  real, allocatable :: press(:, :)

  real, allocatable :: d1(:, :), d2(:, :)

  character(len=80) :: snapfile

  ! >> TMP
  real, allocatable :: tmp(:, : )
  real, allocatable :: uxe(:, : ), uze(:, :)


  dth = dt/h
  n1e = n1+2*npml
  n2e = n2+2*npml

  ! >> Allocate derivative arrays
  allocate (d1(n1e, n2e))
  allocate (d2(n1e, n2e))

  ! >> Allocate velocity fields
  allocate (ux(n1e, n2e))
  allocate (uz(n1e, n2e))

  ! >> Allocate stress fields
  allocate (txx(n1e, n2e))
  allocate (tzz(n1e, n2e))
  allocate (txz(n1e, n2e))

  ! >> Allocate splited velocity fields
  allocate (uxx(n1e, n2e))
  allocate (uxz(n1e, n2e))
  allocate (uzx(n1e, n2e))
  allocate (uzz(n1e, n2e))

  ! >> Allocate splited stress fields
  allocate (txxx(n1e, n2e))
  allocate (txxz(n1e, n2e))
  allocate (tzzx(n1e, n2e))
  allocate (tzzz(n1e, n2e))
  allocate (txzx(n1e, n2e))
  allocate (txzz(n1e, n2e))

  ! >> Allocate pressure field
  allocate (press(n1e, n2e))

  ! >> TEMP
  allocate (tmp(n1e, n2e))
  allocate (uxe(n1e, n2e))
  allocate (uze(n1e, n2e))

  ! >> Initialize velocity fields (including splitted)
  ux(:, :) = 0.
  uz(:, :) = 0.
  uxx(:, :) = 0.
  uxz(:, :) = 0.
  uzx(:, :) = 0.
  uzz(:, : ) = 0.

  uxe(:, :) = 0.
  uze(:, :) = 0.

  ! >> Initialize stress fields (including splitted)
  txx(:, :) = 0.
  tzz(:, :) = 0.
  txz(:, :) = 0.
  txxx(:, :) = 0.
  txxz(:, :) = 0.
  tzzx(:, :) = 0.
  tzzz(:, :) = 0.
  txzx(:, :) = 0.
  txzz(:, :) = 0.

  ! >> Initialize marching and sampling parameters
  full = 0.
  its = 1
  itsnap = 1
  itt = 1
  ets = (nt-1)/(nts-1)
  etsnap = (nt-1)/(ntsnap-1)

  ! >> Start marching
  do it=1,nt
     call cpu_time (start)

     !# >> Ux
     call dxforward (txx, n1e, n2e, d2)
     call dzbackward (txz, n1e, n2e, npml, d1, isurf)

     uxx(:, :) = (((1./dt-pmlx1(:,:))*uxx(:, :) &
          +(1./h)*bux(:, :)*d2(:, :))/(1./dt+pmlx1(:, :)))
     uxz(:, :) = (((1./dt-pmlz0(:,:))*uxz(:, :) &
          +(1./h)*bux(:, :)*d1(:, :))/(1./dt+pmlz0(:, :)))

     !# >> Uz
     call dxbackward (txz, n1e, n2e, d2)
     call dzforward (tzz, n1e, n2e, npml, d1, isurf)

     if (srctype == 2) then
        !# Vertical body force source
        uzx(:, :) = (((1./dt-pmlx0(:,:))*uzx(:, :) &
             +(1./h)*buz(:, :)*d2(:, :))/(1./dt+pmlx0(:, :))) &
             +buz*(tsrc(it)*gsrc(:, :)*dt/(h*h))
     else
        uzx(:, :) = (((1./dt-pmlx0(:,:))*uzx(:, :) &
             +(1./h)*buz(:, :)*d2(:, :))/(1./dt+pmlx0(:, :)))
     end if

     uzz(:, :) = (((1./dt-pmlz1(:,:))*uzz(:, :) &
          +(1./h)*buz(:, :)*d1(:, :))/(1./dt+pmlz1(:, :)))


     call dirichlet (n1e, n2e, uxx, uxz, uzx, uzz)
     ! implement Dirichlet boundary conditions on the four edges of the grid

     ux(:, : ) = uxx(:, :)+uxz(:, :)
     uz(:, : ) = uzx(:, :)+uzz(:, :)

     !write(*,*) sqrt(maxval(ux)**2+maxval(uz)**2)

     !call dirichlet (n1e, n2e, uxx, uxz, uzx, uzz)
     ! implement Dirichlet boundary conditions on the four edges of the grid

     !# PRESSURE
     do i2=1,n2e-1
        do i1=2,n1e-1
           press(i1, i2) = (-lbmu(i1, i2)/h)*(ux(i1,i2)-ux(i1,i2-1) &
                +uz(i1,i2)-uz(i1-1,i2))
        enddo
     enddo

     !# TXX -- TZZ
     if(isurf == 1)then
        do i2=2,n2e
           uz(npml, i2) = uz(npml+1, i2)+&
                lb0(npml+1, i2)/lbmu(npml+1,i2)*&
                (ux(npml+1,i2)-ux(npml+1,i2-1))
        enddo
     endif
     call dxbackward(ux, n1e, n2e, d2)
     call dzbackward(uz, n1e, n2e, npml, d1, isurf)

     !# Explosive source
     if(srctype == 1)then
        txxx(:, :) = (((1./dt-pmlx0(:,:))*txxx(:, :) &
             +(1./h)*lbmu(:, :)*d2(:, :))/(1./dt+pmlx0(:, :))) &
             +(tsrc(it)*gsrc(:,:))/(h*h)*dt
     else
        txxx(:, :) = (((1./dt-pmlx0(:,:))*txxx(:, :) &
             +(1./h)*lbmu(:, :)*d2(:, :))/(1./dt+pmlx0(:, :)))
     end if

     if( isurf == 1 )then
        tmp(:, :) = txxz(:, :)
        txxz(:, :) = (((1./dt-pmlz0(:,:))*txxz(:, :) &
             +(1./h)*lb0(:, :)*d1(:, :))/(1./dt+pmlz0(:, :)))
        txxz(npml+1 ,:) = (((1./dt-pmlx0(npml+1,:))*tmp(npml+1, :) &
             -(1./h)*lb0(npml+1, :)*lb0(npml+1, :)/lbmu(npml+1,:)&
             *(uz(npml+1,:)-uz(npml,:)))/(1./dt+pmlx0(npml+1, :)))
     else
        txxz(:, :) = (((1./dt-pmlz0(:,:))*txxz(:, :) &
             +(1./h)*lb0(:, :)*d1(:, :))/(1./dt+pmlz0(:, :)))
     endif

     txx(:, :) = txxx(:, :) + txxz(:, :)

     if(srctype == 1)then
        !# Explosive source
        tzzx(:, :) = (((1./dt-pmlx0(:,:))*tzzx(:, :) &
             +(1./h)*lb0(:, :)*d2(:, :))/(1./dt+pmlx0(:, :))) &
             +(tsrc(it)*gsrc(:,:))/(h*h)*dt
     else
        tzzx(:, :) = (((1./dt-pmlx0(:,:))*tzzx(:, :) &
             +(1./h)*lb0(:, :)*d2(:, :))/(1./dt+pmlx0(:, :)))
     end if
     tzzz(:, :) = (((1./dt-pmlz0(:,:))*tzzz(:, :) &
          +(1./h)*lbmu(:, :)*d1(:, :))/(1./dt+pmlz0(:, :)))

     tzz(:, :) = tzzx(:, :) + tzzz(:, :)

     if(isurf == 1)then
        tzz(npml+1,:) = 0.
        tzz(npml,:) = -tzz(npml+2,:)
     end if

     !# TXZ
     call dxforward (uz, n1e, n2e, d2)
     call dzforward (ux, n1e, n2e, npml, d1, isurf)

     txzx(:, :) = (((1./dt-pmlx1(:,:))*txzx(:, :) &
          +(1./h)*mue(:, :)*d2(:, :))/(1./dt+pmlx1(:, :)))
     txzz(:, :) = (((1./dt-pmlz1(:,:))*txzz(:, :) &
          +(1./h)*mue(:, :)*d1(:, :))/(1./dt+pmlz1(:, :)))

     txz(:, :) = txzx(:, :)+txzz(:, :)
     if(isurf == 1)then
        txz(npml,:) = -txz(npml+1,:)
        txz(npml-1,:) = -txz(npml+2,:)
     end if

     call cpu_time (finish)
     full = full+(finish-start)
     ! ADD A VERBOSE MODE
     !write(*, * ) it, nt, finish-start, full, sqrt(maxval(ux)**2+maxval(uz)**2), tsrc(it)

     if((itsnap == etsnap .or. it == 1) .and. isnap == 1)then
        itsnap = 1
        if(it < 10)then
           write (snapfile, "(A9,I1)") "snapz0000", it
           open(31, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(31, rec=1) uz
           close(31)
           write (snapfile, "(A9,I1)") "snapx0000", it
           open(32, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(32, rec=1) ux
           close(32)
           write (snapfile, "(A9,I1)") "snapp0000", it
           open(33, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(33, rec=1) press
           close(33)
        else if(it >= 10 .and. it < 100)then
           write (snapfile, "(A8,I2)") "snapz000", it
           open(31, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(31, rec=1) uz
           close(31)
           write (snapfile, "(A8,I2)") "snapx000", it
           open(32, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(32, rec=1) ux
           close(32)
           write (snapfile, "(A8,I2)") "snapp000", it
           open(33, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(33, rec=1) press
           close(33)
        else if(it >= 100 .and. it < 1000)then
           write (snapfile, "(A7,I3)") "snapz00", it
           open(31, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(31, rec=1) uz
           close(31)
           write (snapfile, "(A7,I3)") "snapx00", it
           open(32, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(32, rec=1) ux
           close(32)
           write (snapfile, "(A7,I3)") "snapp00", it
           open(33, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(33, rec=1) press
           close(33)
        else if(it >= 1000 .and. it < 10000)then
           write (snapfile, "(A6,I4)") "snapz0", it
           open(31, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(31, rec=1) uz
           close(31)
           write (snapfile, "(A6,I4)") "snapx0", it
           open(32, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(32, rec=1) ux
           close(32)
           write (snapfile, "(A6,I4)") "snapp0", it
           open(33, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(33, rec=1) press
           close(33)
        else if(it >= 10000 .and. it < 100000)then
           write (snapfile, "(A5,I5)") "snapz", it
           open(31, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(31, rec=1) uz
           close(31)
           write (snapfile, "(A5,I5)") "snapx", it
           open(32, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(32, rec=1) ux
           close(32)
           write (snapfile, "(A5,I5)") "snapp", it
           open(33, file=snapfile, access='direct', recl=n1e*n2e*4)
           write(33, rec=1) press
           close(33)
        end if
     else
        itsnap = itsnap+1
     endif

     !write(*, * ) 'seismograms'
     if(its == ets .or. it == 1)then
        its = 1
        do irec=1,nrec
           ix = recpos(irec, 1)
           iz = recpos(irec, 2)
           recx(itt, irec) = ux(iz,ix) !(ux(iz, ix)+ux(iz,ix-1))/2.
           recz(itt, irec) = uz(iz,ix) !(uz(iz+1, ix)+uz(iz,ix))/2.
           recp(itt, irec) = press(iz, ix)
        end do
        itt = itt + 1
     else
        its = its + 1
     end if

  end do

  deallocate (d1, d2)

  ! >> Free velocity fields
  deallocate (ux, uz)

  ! >> Free splitted velocity fields
  deallocate (uxx, uxz, uzx, uzz)

  ! >> Free stress fields
  deallocate (txx, tzz, txz)

  ! >> Free splitted stress fields
  deallocate (txxx, txxz, tzzx, tzzz, txzx, txzz)

  ! >> Free pressure field
  deallocate (press)

  deallocate (uxe, uze)

end subroutine evolution
