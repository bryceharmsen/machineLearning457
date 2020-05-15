CXX := gcc
CXX_FLAGS:= -O3 -fno-strict-aliasing -DHAVE_SSE2=1 -DSFMT_MEXP=19937

ga: main.o fileIO.o geneticAlgorithm.o randMT.o SFMT.o benchmarkFunctions.o arrMtx.o
	${CXX} ${CXX_FLAGS} -o ga main.o fileIO.o geneticAlgorithm.o randMT.o SFMT.o benchmarkFunctions.o arrMtx.o -lm

main.o: main.c UTIL/fileIO.h UTIL/arrMtx.h UTIL/benchmarks.h GA/geneticAlgorithm.h
	${CXX} ${CXX_FLAGS} -c main.c

fileIO.o: UTIL/fileIO.c UTIL/arrMtx.h UTIL/benchmarks.h GA/geneticAlgorithm.h
	${CXX} ${CXX_FLAGS} -c UTIL/fileIO.c

geneticAlgorithm.o: GA/geneticAlgorithm.c UTIL/benchmarks.h UTIL/fileIO.h
	${CXX} ${CXX_FLAGS} -c GA/geneticAlgorithm.c

randMT.o: UTIL/randMT.c UTIL/arrMtx.h SFMT1.5.1/SFMT.h
	${CXX} ${CXX_FLAGS} -c UTIL/randMT.c

SFMT.o: SFMT1.5.1/SFMT.c
	${CXX} ${CXX_FLAGS} -c SFMT1.5.1/SFMT.c

benchmarkFunctions.o: UTIL/benchmarkFunctions.c UTIL/arrMtx.h
	${CXX} ${CXX_FLAGS} -c UTIL/benchmarkFunctions.c

arrMtx.o: UTIL/arrMtx.c
	${CXX} ${CXX_FLAGS} -c UTIL/arrMtx.c

clean:
	rm -r *.o ./ga