#ifndef BENCHMARKS
#define BENCHMARKS
#include "arrMtx.h"

/*Structures from benchmarkFunctions*/

typedef struct solution {
    dblArr input;
    double fitness;
} solution;

typedef struct solutionArr {
    solution* ptr;
    int rows;
} solutionArr;

/*Functions from benchmarkFunctions*/

double schwefel(dblArr *x);
double deJong1(dblArr *x);
double rosenbrock(dblArr *x);
double rastrigin(dblArr *x);
double griewangk(dblArr *x);
double envSine(dblArr *x);
double stretchVSine(dblArr *x);
double ackleys1(dblArr *x);
double ackleys2(dblArr *x);
double eggHolder(dblArr *x);
double rana(dblArr *x);
double pathological(dblArr *x);
double michalewicz(dblArr *x);
double mastersCos(dblArr *x);
double quartic(dblArr *x);
double levy(dblArr *x);
double step(dblArr *x);
double alpine(dblArr *x);

double functionSelector(dblArr *x, int id);
void populationBulkSolve(dblArr *solutions, dblMtx *matrix, int functionID);
solution createSolution(dblArr *x, int functionID);
int findBestSolution(dblArr *solutions);
void getBestSolutionSubset(dblArr *solutionsOriginal, intArr *selectedSolutions, intArr *bestIndices);
solutionArr convertToSolutions(solution *pairsPtr, dblMtx *population, dblArr *solutions);
void freeSolutionArr(solutionArr * solutions);
solution copySolution(solution *original, double *inputPtr);
void freeSolution(solution *sln);

#endif