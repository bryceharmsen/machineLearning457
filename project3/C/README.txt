 ======================Source Content=============================
 Author: Bryce Harmsen
 Date: 4-21-2019
 ID: 23984439
 Class: CS 471 Optimization with Dr. Davendra
 =================================================================
 ======================SFMT1.5.1 Content==========================
 SFMT ver. 1.5
 SIMD oriented Fast Mersenne Twister(SFMT)

 Mutsuo Saito (Hiroshima University) and
 Makoto Matsumoto (The University of Tokyo)

 Copyright (C) 2006, 2007 Mutsuo Saito, Makoto Matsumoto and Hiroshima
 University.
 Copyright (c) 2012 Mutsuo Saito, Makoto Matsumoto, Hiroshima University
 and The University of Tokyo.
 All rights reserved.

 The (modified) BSD License is applied to this software, see LICENSE.txt
 =================================================================
 
 
 To compile and link from the command-line
 ----------------------------------------------------------------- 
 gcc -O3 -fno-strict-aliasing -DHAVE_SSE2=1 -DSFMT_MEXP=19937 -o proj3 SFMT1.5.1\SFMT.c UTIL\arrMtx.c UTIL\benchmarkFunctions.c UTIL\fileIO.c UTIL\randMT.c GA\geneticAlgorithm.c main.c 
 
 
 Example run from the command-line
 -------------------------------------------------------------------
 proj3 proj3input.txt data.csv 98834
 proj3 <input file> <output file> [<random seed integer>]
 
 
 proj3input.txt is pre-built with input values. Each line of the input file denotes:
 -------------------------------------------------------------------
 for genetic algorithm:
 G \n
   <select function> <elitism rate> <crossover rate probability> <number of crossovers> <mutation probability> <mutation precision> <mutation range> <population> <generations> <dimension> <minimum> <maximum> <benchmark function>
 for differential evolution:
 D \n
   <strategy x> <strategy y> <strategy z> <lambda amplifier> <F amplifier> <crossover rate probability> <number of crossovers> <NP> <iterations> <D> <minimum> <maximum> <benchmark function>

 
 The output file (preferrably .csv), can have any name. The output will be:
 -------------------------------------------------------------------
 <input line 1, sample 1 solution>,<input line 1, sample 2 solution>,...
 <input line 2, sample 1 solution>,<input line 2, sample 2 solution>,...
 ...best solution for each sample set requested from the next line in the input file...
 . .
 .   .
 .      .
 
 
 
 To further randomize outputs
 -------------------------------------------------------------------
 (1) In the compilation line, change the SFMT_MEXP value to one of the
	 predefined SFMT-params*.c values in the SFMT directory.
	 
							-or-
	 
 (2) Provide the optional random seed integer as a fourth command-line argument.
 
 
 
 File System Layout
 -------------------------------------------------------------------
 Harmsen_Project2
	|
	|
	+----Doxygen
	|		|
	|		+----Harmsen_Project3_Documentation.pdf
	|				\
	|				 \
	|				  The Doxygen documentation file for the project
	|
	+----Results
	|		|			  
	|		+----data.csv
	|		|		\
	|		|		 \
	|		|		  The data returned from the program. It has been
	|		|		  reshaped for ease of use.
	|		|
	|		+----stats.csv
	|		|		\
	|		|		 \
	|		|		  The statistics (mean, median, std. dev., range) derived
	|		|		  from each batch of sample data created during program runtime
	|		|
	|		+----Harmsen_Project3.pdf
	|		|		\
	|		|		 \
	|		|		  The report of the experiment, providing an overview of the
	|		|		  project.
	|		|
	|
	+------src
	|		|
	|		+----SFMT1.5.1
	|		|		|
	|		|		+----SFMT.c
	|		|		+----SFMT.h
	|		|		|		\
	|		|		|		 \
	|		|		|		  The particular Mersenne-Twister random generator
	|		|		|		  files creating a link with this project.
	|		|		|
	|		|		+----(see SFMT documentation
	|		|			  for more details)
	|		|
	|		+----main.c
	|		|		\
	|		|		 \
	|		|		  The main file for this project.
	|		|
	|		+----proj3input.txt
	|		|		\
	|		|		 \
	|		|		  The particular inputs used to create the experiment data
	|		|		  of this report. Also, a good example file of how to run
	|		|		  this program
	|		|
	|		+----CMakeLists.txt
	|		|		\
	|		|		 \
	|		|		  The file to point to when generating a CMake build for
	|		|		  project.
	|		|
	|		+----UTIL
	|		|	   \
	|		|		\
	|		|		 The utility files that contain reusable code.
	|		|
	|		+----GA
	|			   \
	|				\
	|				 The files that are tailored to the Genetic Algorithm.
	|
	+----README.txt
			\
			 \
			  This file.