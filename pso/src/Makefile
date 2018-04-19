CC = gcc-6
#LIB = -lgsl -lgslcblas

RDM = $(shell python -c "import numpy, os; print os.path.dirname(numpy.random.__file__)")

DEPS = \
	randgsl.o \
	randpar.o \
	pso_updt.o \
	pso_bound.o \
	pso_init.o

pso.so: $(DEPS)
	$(CC) -std=c11 -shared -Wl,-soname,pso.so.1 -Ofast -o pso.so $^

%.o: %.c
	$(CC) -std=c11 -c -fpic $< -I./ -I$(RDM) -I/usr/include/python2.7/ -L$(RDM) -l:mtrand.so

install: pso.so
	cp pso.so ../libpso.so

clean:
	rm -f *.o pso.so ../libpso*
