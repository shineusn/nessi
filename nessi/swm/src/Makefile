CC = gcc-6

DEPS = \
	swm_modext.o

pso.so: $(DEPS)
	$(CC) -std=c11 -shared -Wl,-soname,swm.so.1 -Ofast -o swm.so $^ -I./

%.o: %.c
	$(CC) -std=c11 -c -fpic $< -I./

install: swm.so
	cp swm.so ../libswm.so

clean:
	rm -f *.o swm.so ../libswm.so
