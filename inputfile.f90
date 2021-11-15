module ELEMENTDATA
    implicit none
    INTEGER :: NELM, MAXNODE
    INTEGER, DIMENSION(:), ALLOCATABLE :: TEN
    INTEGER, DIMENSION(:,:), ALLOCATABLE :: NODE
    DOUBLE PRECISION, DIMENSION(:),ALLOCATABLE :: XELM, YELM
    INTEGER :: NNODE
    DOUBLE PRECISION, DIMENSION(:),ALLOCATABLE :: XNOD, YNOD

end module ELEMENTDATA


program main
    implicit none
    call readFile
    
end program main

subroutine readFile
    use ELEMENTDATA, only:NELM, MAXNODE, XELM, YELM, TEN, NODE, NNODE, XNOD, YNOD 
    implicit none
    INTEGER :: i, j, idum
    open(10,file="ELEMENT.txt",status="old")
    read(10,*)
    read(10,*) NELM, MAXNODE
    allocate(XELM(NELM),YELM(NELM))
    allocate(TEN(NELM))
    allocate(NODE(MAXNODE,NELM))
    read(10,*)
    do i=1,NELM
        read(10,*) idum, XELM(i), YELM(i), TEN(i), (NODE(j,i),j=1,TEN(i))
    end do
    read(10,*)
    read(10,*) NNODE
    allocate(XNOD(NNODE),YNOD(NNODE))
    read(10,*)   
    do i=1,NNODE
        read(10,*) idum, XNOD(i), YNOD(i)
    end do
    close(10)
end subroutine