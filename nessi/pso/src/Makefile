CC = gcc

DEPS = \
	randgsl.o \
	randpar.o \
	pso_updt.o \
	pso_bound.o \
	pso_init.o

pso.so: $(DEPS)
	$(CC) -std=c11 -shared -Wl,-soname,pso.so.1 -Ofast -o pso.so $^ -I./ -lgsl -lgslcblas

%.o: %.c
	$(CC) -std=c11 -c -fpic $< -I./ -lgsl -lgslcblas

install: pso.so
	cp pso.so ../libpso.so

clean:
	rm -f *.o pso.so ../libpso.so
