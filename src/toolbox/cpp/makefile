


FILE = interpolation.cpp
CFLAGS = -Ofast -march=native -std=c++14 -MMD -MP -Wall -DMS_WIN64 -D_hypot=D_hypot
LINUX_COMP = -shared -fPIC
OMPFLAGS = -fopenmp -fopenmp-simd
FFTWFLAGS = -lfftw3
MATHFLAGS = -lm
SHRFLAGS = -fPIC -shared
FLAGS = ${OMPFLAGS} + ${FFTWFLAGS} + ${MATHFLAGS}

build:
		x86_64-w64-mingw32-g++ ${FILE} ${LINUX_COMP} ${CFLAGS} -o test

build:
		x86_64-w64-mingw32-g++ ${FILE} ${LINUX_COMP} ${CFLAGS} -o test
