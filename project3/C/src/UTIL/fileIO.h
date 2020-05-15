#ifndef FILE_IO
#define FILE_IO
#include <stdio.h>
#include "randMT.h"
#include "arrMtx.h"
#include "benchmarks.h"
#include "../GA/geneticAlgorithm.h"

/*Structures from File IO*/

/*Functions from File IO*/

GAinputs createEmptyGAinput(GAinputs *inputsPtr);
GAinputs *parseLineGA(GAinputs *line);
void stdOutArrWriter(double *array, int length);
void stdOutMtxWriter(dblMtx *matrix);
void stdOutSolutionArrWriter(solutionArr *solutions);
void csvMtxWriter(FILE* filePtr, dblMtx matrix);
FILE* csvLineWriter(FILE* filePtr, solution sln, unsigned int duration);
FILE* csvSolutionLines(FILE* filePtr, dblArr solutions, unsigned int *times);
FILE* csvWriteStatement(FILE* filePtr, const char *statement);

#endif