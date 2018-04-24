CC = gcc-6

RDM = $(shell python -c "import numpy, os; print os.path.dirname(numpy.random.__file__)")
PYT = $(shell locate -0 '*/Python.h' | xargs -0 -n1 dirname)
PYT = /usr/include/python2.7

DEPS = \
	randrk.o \
	randpar.o \
	pso_updt.o \
	pso_bound.o \
	pso_init.o

pso.so: $(DEPS)
	$(CC) -std=c11 -shared -Wl,-soname,pso.so.1 -Ofast -o pso.so $^ -I./ -I$(RDM) -I$(PYT) -L$(RDM) -l:mtrand.x86_64-linux-gnu.so

%.o: %.c
	$(CC) -std=c11 -c -fpic $< -I./ -I$(RDM) -I$(PYT) -L$(RDM) -l:mtrand.x86_64-linux-gnu.so

install: pso.so
	cp pso.so ../libpso.so

clean:
	rm -f *.o pso.so ../libpso.so
