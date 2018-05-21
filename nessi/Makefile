all:
	cd grd/src/ && make && make install && cd -
	cd dsp/src/ && make && make install && cd -
	cd modeling/swm/ && f2py -m swmwrap -h swmwrap.pyf src/*.f90 && f2py -c swmwrap.pyf src/*.f90 && cd -

clean:
	cd grd/src/ && make clean && cd -
	cd dsp/src/ && make clean && cd -
	cd modeling/swm/ && rm -f *.so && cd -
