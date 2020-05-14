#ifndef GEN_ALG_H
#define GEN_ALG_H
#include "../UTIL/arrMtx.h"
#include "../UTIL/benchmarks.h"
#include "../UTIL/randMT.h"

/*Constants from algorithms*/

#define TRUE    1
#define FALSE   0

/*Structures from algorithms*/

typedef struct mutation {
    double rate;
    double range;
    int precision;
} mutation;

typedef struct GAinputs {
    FILE *filePtr;
    char algorithm;         //algorithm selector
    char select;            //selection selector
    double elitismRate;     //percentage of population to persist through generation
    double crossoverRate;   //crossover rate
    mutation mutation;      //mutation fields (probability, range and precision)
    int numCrossovers;      //number of crossover points
    int population;         //number of vectors in original matrix
    int generations;        //number of iterations in main algorithm loop
    int dimension;          //number of vector elements
    range range;            //range for each dimension, assuming all dimension have some bounds
    int functionID;         //ID of benchmark function based on functionSelector() switch
} GAinputs;

/*Functions from algorithms*/
void swapData(dblMtx *population, dblMtx *newPopulation);
void reduce(solutionArr *population, solutionArr *newPopulation, int elitismNum);
void tournamentSelect(dblMtx *population, dblArr *solutions, dblMtx *parents);
void rouletteSelect(dblMtx *population, dblArr *solutions, dblMtx *parents);
void rankSelect(dblMtx *population, dblArr *solutions, dblMtx *parents);
void select(dblMtx *population, dblArr *solutions, dblMtx *parents, char selectOption);
int selectParent(dblArr *fitnesses, double totalFitness);
void getFitnesses(dblArr *solutions, dblArr *fitnesses);
double getFitness(dblArr *solutions, dblArr *fitnesses);
void mutate(dblArr *chromosome, mutation *m, range *bounds);
void crossover(dblMtx *parents, dblMtx *offspring, double crossover, int numCrossovers);
void geneticAlgorithm(GAinputs *inputs, dblArr *solutions);

#endif