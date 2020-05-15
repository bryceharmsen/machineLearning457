#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <float.h>
#include "UTIL/fileIO.h"
#include "UTIL/arrMtx.h"
#include "UTIL/benchmarks.h"
#include "GA/geneticAlgorithm.h"

#define SAMPLE_SIZE 30

/**
 * workFlow handles the main outline of the program, bringing
 * together the various tasks into one list of calls.
 * @param input The name of the input file
 * @param output The name of the output file
 * @return int The exit code of the function
 */
int workFlow(char* input, char* output) {
    FILE* inFilePtr;
	inFilePtr = fopen(input, "r");

    if(inFilePtr == NULL) {
        fprintf(stderr, "ERROR: The input file provided does not exist.\n");
        return 1;
    }

	FILE* outFilePtr;
	outFilePtr = fopen(output, "w");
    
    clock_t startTime, endTime;
    double duration;

    int end = FALSE;
    int counter = 0;
    while(!end) {
        char algorithm = 0;
	    fscanf(inFilePtr, "%c\n", &algorithm);
        GAinputs genInputs = *((GAinputs *) malloc(sizeof(GAinputs)));
        solutionArr *solutions = NULL;
        double *bestPtr = NULL;
        dblArr bestSolutions;
        double best = 0;
        unsigned int start, duration;

        unsigned int *times = NULL;
        if (algorithm == '0') {
            end = TRUE;
            printf("Reached end of file.\n");
            continue;
        }
        startTime = clock();
        switch(algorithm) {
            case 'G':   //Genetic Algorithm
                genInputs.filePtr = inFilePtr;
                parseLineGA(&genInputs);
                genInputs.algorithm = algorithm;
                times = (unsigned int *) calloc(genInputs.generations, sizeof(unsigned int));
                bestSolutions = createEmptyArray(bestPtr, genInputs.generations);
                fprintf(outFilePtr, "Fn%d GA %c,", genInputs.functionID, genInputs.select);
                for(int i = 0; i < SAMPLE_SIZE; i++) {
                    geneticAlgorithm(&genInputs, &bestSolutions);
                    //outFilePtr = csvSolutionLines(outFilePtr, bestSolutions, times);
                    best = bestSolutions.ptr[bestSolutions.length - 1];//findBestSolution(&bestSolutions);
                    fprintf(outFilePtr, "%lf,", best);
                }
                printf("Printed and finished input file line %d.\n", counter);
                counter += 2;
                break;
        }
        endTime = clock();
        duration = difftime(endTime, startTime);//((double) (endTime - startTime)) / (CLOCKS_PER_SEC / 1000.0);
        printf("time: %ld\n", duration);

        fprintf(outFilePtr,"\n");
        free(times);
        free(solutions);
        free(bestSolutions.ptr);
    }
    printf("Closing files...\n");
    fclose(inFilePtr);
    fclose(outFilePtr);

    return 0;
}

int main(int argc, char* argv[]) {
	if(argc != 3 && argc != 4) {
		printf("Wrong number of arguments. Arguments should be: \n");
		printf("<input file> <output file> [<random seed integer>]\n");
		return 1;
	}
	char* input = argv[1];
	char* output = argv[2];

    if(argc == 4) {
        sfmt_init_gen_rand(&sfmt, atoi(argv[3]));
    } else {
        sfmt_init_gen_rand(&sfmt, 1234);
    }
    printf("Input file: %s\nOutput file: %s\n", input, output);
    int err = workFlow(input, output);
    printf("exit status: %d\n", err);
    return err;
}