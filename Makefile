CC = gcc-6.3.0

#SRCS_C = pso/randgsl.c pso/randpar.c pso/init_swarm.c

#OBJS = $(SRCS_C:.c=.o)

LIB = -lgsl

all: libpso

libpso: randgsl.o randpar.o pso_updt.o pso_bound.o pso_init.o
	$(CC) -std=c11 -shared -Wl,-soname,libpso.so.1 -Ofast -o libpso.so $^ -lgsl

%.o: pso/%.c
	$(CC) -std=c11 -c -fpic $< -Ipso/ $(LIB)

clean:
	rm -f *.o pso/*.o libpso.so
