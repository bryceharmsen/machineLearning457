#include <stdio.h>
#include "arrMtx.h"
#include "fileIO.h"
#include "benchmarks.h"
#include "../GA/geneticAlgorithm.h"

GAinputs createEmptyGAinput(GAinputs *inputsPtr) {
	inputsPtr = (GAinputs *) malloc(sizeof(GAinputs));
	inputsPtr->algorithm = '0';
	inputsPtr->crossoverRate = 0;
	inputsPtr->dimension = 0;
	inputsPtr->elitismRate = 0;
	inputsPtr->filePtr = NULL;
	inputsPtr->functionID = 0;
	inputsPtr->generations = 0;
	inputsPtr->mutation.precision = 0;
	inputsPtr->mutation.range = 0;
	inputsPtr->mutation.rate = 0;
	inputsPtr->numCrossovers = 0;
	inputsPtr->population = 0;
	inputsPtr->range.min = 0;
	inputsPtr->range.max = 0;
	inputsPtr->select = '0';
	return *inputsPtr;
}

/**
 * parseLine parses the arguments from one line of the input file and assigns
 * them to fields within the line structure.
 * @param fPtr The pointer to the input file
 * @return fLine The line structure containing the arguments from a line in
 * 			the input file
 */
GAinputs *parseLineGA(GAinputs *line) {
	fscanf(line->filePtr, "%c %lf %lf %d %d %lf %lf %d %d %d %lf %lf %d\n",
				 &line->select,
				 &line->elitismRate,
				 &line->crossoverRate,
				 &line->numCrossovers,
				 &line->mutation.precision,
				 &line->mutation.range,
				 &line->mutation.rate,
				 &line->population,
				 &line->generations,
				 &line->dimension,
				 &line->range.min,
				 &line->range.max,
				 &line->functionID);
	return line;
}

void stdOutArrWriter(double *array, int length) {
	for(int i = 0; i < length; i++) {
		printf("%lf ", array[i]);
	}
	printf("\n");
}

/**
 * Prints the given matrix to standard out.
 * @param matrix The dblMtx struct to write
 */
void stdOutMtxWriter(dblMtx *matrix) {
	for(int i = 0; i < matrix->rows; i++) {
		for(int j = 0; j < matrix->cols; j++) {
			printf("%lf ", matrix->ptr[i][j]);
		}
		printf("\n");
	}
}

void stdOutSolutionArrWriter(solutionArr *solutions) {
	for(int i = 0; i < solutions->rows; i++) {
		printf("inputs:\n");
		for(int j = 0; j < solutions->ptr->input.length; j++) {
			printf("%lf ", solutions->ptr[i].input.ptr[j]);
		}
		printf("\nsolution: %lf\n", solutions->ptr[i].fitness);
	}
}

/**
 * Prints the given matrix to a specified .csv file.
 * @param fileName A string containing the name of the file (including
 * .csv) 
 * @param matrix The dblMtx struct to write
 */
void csvMtxWriter(FILE* filePtr, dblMtx matrix) {
	for(int i = 0; i < matrix.rows; i++) {
		for(int j = 0; j < matrix.cols; j++) {
			fprintf(filePtr, "%lf,", matrix.ptr[i][j]);
		}
		fprintf(filePtr, "\n");
	}
}

/**
 * Prints the given values to a line in the specified .csv file pointer.
 * Number of columns must be defined.
 * @param filePtr The pointer to the .csv file
 * @param sln The solution to write to a file
 * @param duration The time that passed when calculating the solution
 * @return The pointer to the open file
 */
FILE* csvLineWriter(FILE* filePtr, solution sln, unsigned int duration) {
	fprintf(filePtr, "%d,%lf,", duration, sln.fitness);
	for(int i = 0; i < sln.input.length; i++) {
		fprintf(filePtr, "%lf,", sln.input.ptr[i]);
	}
	fprintf(filePtr, "\n");
	return filePtr;
}

/**
 * Prints a line of solutions to a file, built with preference towards a .csv file.
 * @param filePtr The pointer to the file
 * @param solutions The dblArr struct cointaining the solutions
 * @param times The times that passed when calculating the solution
 * @return The pointer to the open file
 */
FILE* csvSolutionLines(FILE* filePtr, dblArr solutions, unsigned int *times) {
	printf("Solutions printed to file: ");
	for(int i = 0; i < solutions.length; i++) {
		printf("%lf, ", solutions.ptr[i]);
	}
	printf("\n");
	for(int i = 0; i < solutions.length; i++) {
		fprintf(filePtr, "%lf,", solutions.ptr[i]);
	}
	fprintf(filePtr, "\n");

	/*printf("\n\nTIMES: ");
	fprintf(filePtr, "Times: ,");
	for(int i = 0; i < solutions.length; i++) {
		fprintf(filePtr, "%g,", times[i]);
		printf("%g, ", times[i]);
	}
	printf("\n\n");*/
	fprintf(filePtr, "\n");
	return filePtr;
}

/**
 * Writes a general statement contained in a string to the given file.
 * @param filePtr The pointer to the file
 * @param statement The string to be written to the file
 * @return The pointer to the open file
 */
FILE* csvWriteStatement(FILE* filePtr, const char *statement) {
	fprintf(filePtr, "%s", statement);
	return filePtr;
}