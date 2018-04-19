CC = gcc-6.3.0
LIB = -lgsl -lgslcblas

all: libpso libgrd libdsp

libpso: randgsl.o randpar.o pso_updt.o pso_bound.o pso_init.o
	$(CC) -std=c11 -shared -Wl,-soname,lib/libpso.so.1 -Ofast -o lib/libpso.so $^ -lgsl -lgslcblas

%.o: pso/%.c
	$(CC) -std=c11 -c -fpic $< -Ipso/ $(LIB)

libgrd: grd_vrn.o grd_idw.o grd_ds1.o grd_ds2.o
	$(CC) -std=c11 -shared -Wl,-soname,lib/libgrd.so.1 -Ofast -o lib/libgrd.so $^

%.o: grd/%.c
	$(CC) -std=c11 -c -fpic $< -Igrd/

libdsp: dsp_core.o dsp_phase.o dsp_masw.o dsp_gauss.o dsp_gsmooth.o
	$(CC) -std=c11 -shared -Wl,-soname,lib/libdsp.so.1 -Ofast -o lib/libdsp.so $^

%.o: dsp/%.c
	$(CC) -std=c11 -c -fpic $< -Idsp/

clean:
	rm -f *.o pso/*.o lib/libpso.so grd/*.o lib/libgrd.so dsp/*.o lib/libdsp.so
