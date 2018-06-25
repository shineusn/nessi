all:
	cd modbuilder/interp2d/src/ && make && make install && cd -
	cd modeling/swm/ && f2py -m swmwrap -h swmwrap.pyf src/*.f90 && f2py -c swmwrap.pyf src/*.f90 && cd -

clean:
	cd modbuilder/interp2d/src/ && make clean && cd -
	cd modeling/swm/ && rm -f *.so && cd -
