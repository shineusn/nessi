all:
	cd nessi && make && cd -

clean:
	cd nessi/modbuilder/interp2d/src/ && make clean && cd -
	cd nessi/signal/dsp/src/ && make clean && cd -
	cd nessi/modeling/swm/ && rm -f *.so && cd -
