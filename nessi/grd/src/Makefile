CC = gcc

DEPS = \
	grd_vrn.o \
	grd_idw.o \
	grd_ds1.o \
	grd_ds2.o

pso.so: $(DEPS)
	$(CC) -std=c11 -shared -Wl,-soname,grd.so.1 -Ofast -o grd.so $^ -I./

%.o: %.c
	$(CC) -std=c11 -c -fpic $< -I./

install: grd.so
	cp grd.so ../libgrd.so

clean:
	rm -f *.o pso.so ../libgrd.so
