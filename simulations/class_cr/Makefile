# CLASS-CR Makefile
CC ?= gcc
CFLAGS = -O3 -Wall -fopenmp -Iinclude -lm

SRCS = source/background.c source/thermodynamics.c source/perturbations.c source/bessel.c source/spectra.c source/spectra_exact.c source/matter.c source/main.c
OBJS = $(SRCS:.c=.o)
TARGET = class_cr

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(CFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f source/*.o $(TARGET) class_cr.exe class_cr_cl.dat
