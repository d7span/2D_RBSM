module ELEMENTDATA
    implicit none
    INTEGER :: NELM, MAXNODE
    INTEGER, DIMENSION(:), ALLOCATABLE :: TEN
    INTEGER, DIMENSION(:,:), ALLOCATABLE :: NODE
    DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: XYZ
    INTEGER :: NNOD
    DOUBLE PRECISION, DIMENSION(:),ALLOCATABLE :: XNOD, YNOD

    !材料データ
    INTEGER :: NMAT
    DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: EM
    DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: POIS
    DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: FT
    DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: FC
    DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: PHI0
    DOUBLE PRECISION, DIMENSION(:), ALLOCATABLE :: GFT0
    !載荷板データ
    INTEGER :: NPLATE
    DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: XYZ_PLT

    INTEGER :: NLINE
    INTEGER, DIMENSION(:,:), ALLOCATABLE :: ILINK

end module ELEMENTDATA

module FLAGINFO
    implicit none
    INTEGER :: ISTMX, ITRMX
    DOUBLE PRECISION :: CNVRG
end module FLAGINFO

module MATRIX_EQUATION_DATA
    implicit none
    INTEGER :: IELM
    INTEGER :: NDOF
    DOUBLE PRECISION :: D0 
end module MATRIX_EQUATION_DATA

program main
    implicit none
    call readFile
    call makeLINE
    call calEP
    
end program main

subroutine readFile
    use ELEMENTDATA, only:NMAT, EM, POIS, FT, FC, PHI0, GFT0, NPLATE, XYZ_PLT, NELM, MAXNODE, XYZ, TEN, NODE, NNOD, XNOD, YNOD
    use FLAGINFO, only:ISTMX, ITRMX, CNVRG
    use MATRIX_EQUATION_DATA, only:IELM, NDOF, D0
    implicit none
    INTEGER :: i, j, idum
    INTEGER :: N1
    INTEGER :: M
    INTEGER :: ITEMP(3) 
    INTEGER :: NEL1

    !=======================
    !READ CONTROL.txt
    !=======================
    write(*,*) "read CONTROL.txt"
    open(10,file="CONTROL.txt",status="old")
    read(10,*) !解析制御データ
    read(10,*) ISTMX, ITRMX, CNVRG
    
    read(10,*) !変位制御データ
    read(10,*) IELM, NDOF, D0
    read(10,*) !材料データ
    read(10,*) NMAT

    allocate(EM(NMAT),POIS(NMAT))
    allocate(FT(NMAT),FC(NMAT))
    allocate(PHI0(NMAT))
    allocate(GFT0(NMAT))
   
    do i = 1, NMAT
        read(10,*) idum, EM(i), POIS(i), FT(i), FC(i), PHI0(i), GFT0(i)
    end do
    read(10,*) !載荷板データ
    read(10,*) NPLATE
    allocate(XYZ_PLT(2,NPLATE))
    do i = 1, NPLATE
        read(10,*) idum, (XYZ_PLT(j,i), j=1,2)
    end do
    read(10,*) !境界条件
    read(10,*) M
    do i = 1, M
        read(10,*) idum, NEL1, (ITEMP(j), j=1,3)
    end do
    close(10)

    !=======================
    !READ ELEMENT.txt
    !=======================
    write(*,*) "read ELEMENT.txt"
    open(10,file="ELEMENT.txt",status="old")
    read(10,*)
    read(10,*) NELM, MAXNODE
    N1 = NELM + NPLATE
    allocate(XYZ(2,N1))
    allocate(TEN(NELM))
    allocate(NODE(MAXNODE,NELM))
    read(10,*)
    do i=1,NELM
        read(10,*) idum, (XYZ(j,i), j=1,2), TEN(i), (NODE(j,i), j=1,TEN(i))
    end do
    read(10,*)
    read(10,*) NNOD
    allocate(XNOD(NNOD),YNOD(NNOD))
    read(10,*)   
    do i = 1, NNOD
        read(10,*) idum, XNOD(i), YNOD(i)
    end do
    close(10)

end subroutine

subroutine makeLINE
    use ELEMENTDATA, only:NELM, TEN, NODE, NNOD, ILINK, NLINE
    implicit none
    INTEGER :: i, j, k, idum
    INTEGER :: IPO1, IPO2
    INTEGER :: flag_temp

    NLINE = 0
    allocate(ILINK(2,2*NNOD))
    do i = 1, NELM
        do j = 1, TEN(i)
            flag_temp = 0
            if ( j /= TEN(i) ) then
                IPO1 = NODE(j,i)
                IPO2 = NODE(j+1,i)    
            else
                IPO1 = NODE(j,i)
                IPO2 = NODE(1,i) 
            end if 
            if ( IPO1 > IPO2 ) then
                idum = IPO1
                IPO1 = IPO2
                IPO2 = idum
            end if
            !write(*,*) IPO1, IPO2
            do k = 1, NLINE
                if ( (IPO1 == ILINK(1,k)) .and. (IPO2 == ILINK(2,k)) ) then
                    flag_temp = 1
                    exit
                end if
            end do
            if ( flag_temp == 0 ) then
                NLINE = NLINE + 1   
                ILINK(1,NLINE) = IPO1
                ILINK(2,NLINE) = IPO2
            end if
        end do    
    end do
end subroutine

subroutine calEP
    use ELEMENTDATA, only:NLINE
    implicit none
    INTEGER :: i
    INTEGER :: IE1, IE2
    do i = 1, NLINE
        

        
    end do
end subroutine