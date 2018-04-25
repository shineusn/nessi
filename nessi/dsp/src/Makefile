CC = gcc-6

DEPS = \
	dsp_core.o \
	dsp_gauss.o \
	dsp_gsmooth.o \
	dsp_masw.o \
	dsp_phase.o

dsp.so: $(DEPS)
	$(CC) -std=c11 -shared -Wl,-soname,dsp.so.1 -Ofast -o dsp.so $^ -I./ -lfftw3

%.o: %.c
	$(CC) -std=c11 -c -fpic $< -I./ -lfftw3

install: dsp.so
	cp dsp.so ../libdsp.so

clean:
	rm -f *.o dsp.so ../libdsp.so
