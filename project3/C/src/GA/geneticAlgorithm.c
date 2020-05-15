#include <time.h>
#include <stdio.h>
#include <math.h>
#include <float.h>
#include "../GA/geneticAlgorithm.h"
#include "../UTIL/benchmarks.h"
#include "../UTIL/fileIO.h"

#define max(a,b) (((a) > (b)) ? (a) : (b))
#define min(a,b) (((a) < (b)) ? (a) : (b))

static struct timespec t;

/**
 * A comparison function for qsort, modeled after a function
 * built by Steven S. Skiena in his book "The Algorithm Design
 * Manual". This reports to qsort whether ints a and b are sorted
 * already.
 * @param a
 * @param b
 */
int intIncreaseSortComparison(const void *a, const void *b) {
    int *m = (int *) a;
    int *n = (int *) b;
    if (*m > *n) {
        return 1;
    } else if (*m < *n) {
        return -1;
    }

    return 0;
}

/**
 * A comparison function for qsort, roughly based on function
 * published by Steven S. Skiena in "The Algorithm Design Manual".
 * This reports to qsort whether ints a and b are sorted
 * already. The comparison is based on the fitness of a solution.
 * @param a
 * @param b
 */
int solutionIncreaseSortComparison(const void *a, const void *b) {
    solution *m = (solution *) a;
    solution *n = (solution *) b;
    if (m->fitness > n->fitness) {
        return 1;
    } else if (m->fitness < n->fitness) {
        return -1;
    }
    
    return 0;
}

/**
 * Reduce keeps the most elite population vectors, then replaces the rest of the population
 * vectors with the best newPopulation vectors. So in population, population[0] through
 * population[elitismNum - 1] are the best from the population matrix, and population[elitismNum]
 * through population[length - 1] are the best from the newPopulation matrix.
 * @param population
 * @param newPopulation
 * @param elitismNum
 */
void reduce(solutionArr *population, solutionArr *newPopulation, int elitismNum) {
    //sortByCostAscending(population)
    qsort(population->ptr, population->rows, sizeof(solution), solutionIncreaseSortComparison);

    //sortByCostAscending(newPopulation)
    qsort(newPopulation->ptr, newPopulation->rows, sizeof(solution), solutionIncreaseSortComparison);

    //keeping newPopulation
    int cols = population->ptr[0].input.length;
    for (int newPopRow = (population->rows - 1 - elitismNum), popRow = 0; popRow < elitismNum; popRow++, newPopRow++) {
        copyPtr(population->ptr[popRow].input.ptr, newPopulation->ptr[newPopRow].input.ptr, cols);
        newPopulation->ptr[newPopRow].fitness = population->ptr[popRow].fitness;
    }
}

/**
 * Simulating a tournament, tournamentSelect chooses a random number of random population vectors to include in
 * the tournament, and the two vectors with the best fitness solutions are copied into the parents dblMtx.
 * @param population The population that the parents are selected from
 * @param solutions The respective fitness solutions for each population vector
 * @param parents The dblMtx that the selected vectors will be placed in
 */
void tournamentSelect(dblMtx *population, dblArr *solutions, dblMtx *parents) {
    int popSize = population->rows;
    
    //determine the number of candidates to be included in tournament
    int lowPressure = max(parents->rows, popSize/4);
    int highPressure = max(parents->rows, 3*popSize/4);
    range pressureRange = {lowPressure, highPressure};
    int selectionPressure = (int) randNumByRange(pressureRange);

    //assign random selection candidate indices to selectionIndices
    int *selectionIndicesPtr = NULL;
    intArr selectionIndices = createEmptyIntArr(selectionIndicesPtr, selectionPressure);
    range popRange = {0, popSize - 1};
    exclusiveRandoms(&selectionIndices, &popRange, -1);

    //choose the best parents.length number of these random selection candidates
    int *parentIndicesPtr = NULL;
    intArr parentIndices = createEmptyIntArr(parentIndicesPtr, parents->rows);
    getBestSolutionSubset(solutions, &selectionIndices, &parentIndices);
    for(int i = 0; i < parents->rows; i++) {
        copyPtr(population->ptr[parentIndices.ptr[i]], parents->ptr[i], population->cols);
    }
    free(selectionIndices.ptr);
    free(parentIndices.ptr);
}

/**
 * rouletteSelect simulates a roulette wheel, with proportionate sections of the wheel
 * given to the vectors with the best fitness. The wheel is spun twice, and the two
 * population vectors chosen are assigned to the parents dblMtx.
 * @param population The population that the parents are selected from
 * @param solutions The respective fitness solutions for each population vector
 * @param parents The dblMtx that the selected vectors will be placed in
 */
void rouletteSelect(dblMtx *population, dblArr *solutions, dblMtx *parents) {
    double *probabilitiesPtr = NULL;
    dblArr probabilities = createEmptyArray(probabilitiesPtr, solutions->length);
    double fitSum = sum(solutions);
    int indexOfBest = findBestSolution(solutions);
    double best = min(0, solutions->ptr[indexOfBest]);
    //calculate probabilities with either 0 as the floor, or, if containing a negative lowest, best_probability = 100%
    for (int i = 0; i < solutions->length; i++) {
        probabilities.ptr[i] = 1 - (solutions->ptr[i] - best) / (fitSum - best*solutions->length); // (sum_adjusted - current_adjusted) / (sum_adjusted)
    }
    //normalize probabilities
    double probSum = sum(&probabilities);
    for (int i = 0; i < probabilities.length; i++) {
        probabilities.ptr[i] /= probSum;
    }
    //set probability ranges within probabilities array
    probabilities.ptr[probabilities.length - 1] = 1 - probabilities.ptr[probabilities.length - 1];
    for (int i = probabilities.length - 2; i >= 0; i--) {
        probabilities.ptr[i] = probabilities.ptr[i + 1] - probabilities.ptr[i];
    }
    //select based on probability weights
    range rateRng = {0, 1};
    for (int parent = 0; parent < parents->rows; parent++) {
        double random = randNumByRange(rateRng);
        for (int i = 0; i < probabilities.length; i++) {
            if (random >= probabilities.ptr[i]) {
                copyPtr(population->ptr[i], parents->ptr[parent], population->cols); //assign chosen population candidate to parent based on solution probabilites
            }
        }
    }
}

/**
 * getFitnesses calculates the fitness, 1 / (1 + |cost|), for each solution and
 * assigns the values to the fitnesses dblArr.
 * @param solutions The solution costs to be recalculated
 * @param fitnesses The empty fitnesses dblArr that will hold the calculated fitnesses
 */
void getFitnesses(dblArr *solutions, dblArr *fitnesses) {
    for (int s = 0; s < solutions->length; s++) {
        double cost = solutions->ptr[s];
        if (cost >= 0) {
            fitnesses->ptr[s] = 1.0 / (1 + cost);
        } else {
            fitnesses->ptr[s] = 1.0 / (1 + fabs(cost));
        }
    }
}

/**
 * getFitness finds the sum of all fitnesses and returns this double value. This function
 * requires a filled solutions dblArr, and an empty fitnesses dblArr that will be filled
 * with respective recalculated fitness values.
 * @param solutions The solution costs to be recalculated
 * @param fitnesses The empty fitnesses dblArr that will be used to calculate the total sum
 */
double getFitness(dblArr *solutions, dblArr *fitnesses) {
    double totalFitness = 0;
    getFitnesses(solutions, fitnesses);
    totalFitness = sum(fitnesses);
    return totalFitness;
}

/**
 * The heart of rankSelect, selectParent randomly selects population vector index. This 
 * function is meant to make each index equally as likely to be chosen.
 * @param fitnesses The fitnesses used to randomly select an index
 * @param totalFitness The total of the fitnesses provided
 */
int selectParent(dblArr *fitnesses, double totalFitness) {
    range rng = {0, totalFitness};
    double random = randNumByRange(rng);
    int selection = 0;
    while (selection < (fitnesses->length - 1) && random > 0) {
        random -= fitnesses->ptr[selection];
        selection++;
    }
    return selection;
}

/**
 * rankSelect randomly selects population vectors. This function is meant to make each
 * population vector equally as likely to be chosen.
 * @param population The population of parent candidates
 * @param solutions The respective solutions for the population provided
 * @param parents The empty dblMtx that will be filled with parent vectors
 */
void rankSelect(dblMtx *population, dblArr *solutions, dblMtx *parents) {
    int i[2];
    double *fitnessesPtr = NULL;
    dblArr fitnesses = createEmptyArray(fitnessesPtr, solutions->length);
    double totalFitness = getFitness(solutions, &fitnesses);
    i[0] = selectParent(&fitnesses, totalFitness);
    i[1] = selectParent(&fitnesses, totalFitness);
    while (i[0] == i[1]) {
        i[1] = selectParent(&fitnesses, totalFitness);
    }
    for (int row = 0; row < parents->rows; row++) {
        copyPtr(population->ptr[i[row % 2]], parents->ptr[row], parents->cols);
    }
    free(fitnesses.ptr);
}

/**
 * Selects either roulette, tournament, or rank select based on the user's choice.
 * These selection functions choose two parents from the provided population matrix.
 * @param population The population of parent candidates
 * @param solutions The respective solutions for the provided population
 * @param parents The empty dblMtx that will be filled with vectors
 * @param selectOptions The type of selection method. Either 'r' (roulette), 't' (tournament),
 * or 'k' (rank).
 */
void abstractSelect(dblMtx *population, dblArr *solutions, dblMtx *parents, char selectOption) {
    switch(selectOption) {
        default:
            printf("Selection defaulting to roulette select...\n");
        case 'r':
            rouletteSelect(population, solutions, parents);
            break;
        case 't':
            tournamentSelect(population, solutions, parents);
            break;
        case 'k':
            rankSelect(population, solutions, parents);
            break;
    }
}

/**
 * Based on the number of crossovers, join will create the appropriate number of
 * offspring based on the two parents, randomly creating crossover points and
 * assigning all combinations to the offspring dblMtx. Be sure to create an empty
 * offspring dblMtx with (2 ^(numCrossovers) - 1) rows.
 * @param parentA The first parent to be used in the crossover joins
 * @param parentB The second parent to be used in the crossover joins
 * @param offspring The empty offspring dblMtx to be filled with parent combinations
 * @param numCrossovers The number of crossovers to perform on the parents (this
 * also determines the number of rows in the offspring matrix)
 */
void join(double* parentA, double* parentB, dblMtx *offspring, int numCrossovers) {
    int crossoverMultiplier = pow(2, numCrossovers) - 1;
    int dim = offspring->cols;
    range dimRng = {1, dim - 1};

    int *crossoversPtr = NULL;
    intArr crossovers = createEmptyIntArr(crossoversPtr, numCrossovers + 1);
    //get and sort random indices to perform crossover joins
    exclusiveRandoms(&crossovers, &dimRng, -1);
    qsort(crossovers.ptr, crossovers.length, sizeof(int), intIncreaseSortComparison);
    
    //the last crossover point is the dimension of the population
    crossovers.ptr[crossovers.length - 1] = dim;
    
    int *comboListPtr = NULL;
    intArr comboList = createEmptyIntArr(comboListPtr, numCrossovers);
    //for every combination of joins
    for (int combo = 1; combo <= crossoverMultiplier * 2; combo++) {
        int currCombo = combo; //so currCombo can be corrupted safely
        //for each crossover index, set which sections pull from which parent (either p0 or p1)
        for (int crossoverID = comboList.length - 1; crossoverID >= 0; crossoverID--) {
            comboList.ptr[crossoverID] = currCombo % 2;
            currCombo /= 2;
        }

        //for each section (beginning to crossover1, cr1 to cr2, ..., crN to end), copy from correct parent
        int i = 0;
        for (int section = 0; section < crossovers.length; section++) {
            int parentID = comboList.ptr[section];
            //for correct parent, copy indexed value while index is smaller than crossover point
            while (i < crossovers.ptr[section]) {
                //if parentID == 0, use from parentA
                double* parent = parentA;
                //otherwise use from parent B
                if (parentID == 1) {
                    parent = parentB;
                }
                offspring->ptr[combo - 1][i] = parent[i];
                i++;
            }
        }
    }

    free(crossovers.ptr);
    free(comboList.ptr);
}

/**
 * Crossover determines whether or not any crossover joins should happen,
 * and if so, calls for these joins.
 * @param parents The parents used to create offpsring
 * @param offspring The empty array that will contain the offspring
 * @param crossover The crossover rate chosen by the user
 * @param numCrossovers The number of crossovers to perform in join
 */
void crossover(dblMtx *parents, dblMtx *offspring, double crossover, int numCrossovers) {
    int crossoverMultiplier = pow(2, numCrossovers) - 1;
    range rateRng = {0, 1};
    if (randNumByRange(rateRng) < crossover) {
        join(parents->ptr[0], parents->ptr[1], offspring, numCrossovers);
    } else {
        for(int row = 0; row < offspring->rows; row += 2) {
            int A = row % parents->rows;
            int B = (row + 1) % parents->rows;
            copyPtr(parents->ptr[A], offspring->ptr[row], parents->cols);
            copyPtr(parents->ptr[B], offspring->ptr[row + 1], parents->cols);
        }
    }
}

/**
 * Mutates each element in the chromosome vector provided.
 * @param chromosome The vector to be mutated
 * @param m The mutation parameters that give particular shape to the mutation
 * @param bounds The bounds provided for the benchmark function
 */
void mutate(dblArr *chromosome, mutation *m, range *bounds) {
    range rateRng = {0, 1};
    range sgnSwitchRng = {-1, 1};
    for (int i = 0; i < chromosome->length; i++) {
        if (randNumByRange(rateRng) < m->rate) {
            chromosome->ptr[i] += randNumByRange(sgnSwitchRng) 
                                    * (bounds->max - bounds->min) 
                                        * m->range 
                                            * pow(2, (-1 * randNumByRange(rateRng) * m->precision));
        }
    }
}

/**
 * Genetic Algorithm uses selection, mutation, and reduction in generations to create
 * more optimal solutions in the solution space of the benchmark function selected.
 * @param inputs The required user inputs that run GA
 * @param bestSolutions The empty dblArr that will be filled with the best solution
 * for each generation
 */
void geneticAlgorithm(GAinputs *inputs, dblArr *bestSolutions) {
    int elitism = (int) (inputs->elitismRate * inputs->population);
    //initialize population
    double **populationPtr = NULL;
    dblMtx population = createEmptyMatrix(populationPtr, inputs->population, inputs->dimension);
    fillMatrix(&population, inputs->range);

    double *solutionsPtr = NULL;
    dblArr solutions = createEmptyArray(solutionsPtr, inputs->population);
    
    //evaluate population
    
    //new population matrix for iterations
    double **parentsPtr = NULL;
    dblMtx parents = createEmptyMatrix(parentsPtr, 2, population.cols);
    
    int offspringMultiplier = pow(2, inputs->numCrossovers) - 1;
    double **offspringPtr = NULL;
    dblMtx offspring = createEmptyMatrix(offspringPtr, parents.rows * offspringMultiplier, population.cols);
    populationBulkSolve(&solutions, &population, inputs->functionID);
    for(int t = 0; t < inputs->generations; t++) { 
        double **newPopulationPtr = NULL;
        dblMtx newPopulation = createEmptyMatrix(newPopulationPtr, inputs->population * offspringMultiplier, inputs->dimension);
        for(int s = 0; s < inputs->population - 1; s += 2) {
            //select parents based on selection method chosen in switch
            abstractSelect(&population, &solutions, &parents, inputs->select);
            //perform crossover with probability CR
            crossover(&parents, &offspring, inputs->crossoverRate, inputs->numCrossovers);
            //perform mutation with mutation parameters M
            dblArr eachOffspring = {NULL, population.cols};
            for(int OS = 0; OS < offspring.rows; OS++) {
                eachOffspring.ptr = offspring.ptr[OS];
                mutate(&eachOffspring, &inputs->mutation, &inputs->range);
                //add offspring to temp population matrix
                copyPtr(offspring.ptr[OS], newPopulation.ptr[s*offspringMultiplier + OS], newPopulation.cols);
            }
        }
        //evaluate fitness for each solution
        double *newSolutionsPtr = NULL;
        dblArr newSolutions = createEmptyArray(newSolutionsPtr, newPopulation.rows);
        populationBulkSolve(&newSolutions, &newPopulation, inputs->functionID);
        //elitist combine of population and new population
        solution *popSolPtr = NULL;
        solutionArr popSolutionSet = convertToSolutions(popSolPtr, &population, &solutions);

        solution *newSolPtr = NULL;
        solutionArr newSolutionSet = convertToSolutions(newSolPtr, &newPopulation, &newSolutions);
        reduce(&popSolutionSet, &newSolutionSet, elitism);

        //create solutionArr copy
        for(int i = 0; i < solutions.length; i++) {
            solutions.ptr[i] = newSolutionSet.ptr[i].fitness;
            for (int j = 0; j < population.cols; j++) {
                population.ptr[i][j] = newSolutionSet.ptr[i].input.ptr[j];
            }
        }

        int bestFitnessIndex = 0;
        int oldBest = population.rows - elitism - 1;
        if (solutions.ptr[oldBest] < solutions.ptr[0]) {
            bestFitnessIndex = oldBest;
        }
        
        //store the best solution for later, to be graphed and analyzed
        bestSolutions->ptr[t] = solutions.ptr[bestFitnessIndex];
        //copyMatrix(&newPopulation, &population);
        free(newSolutions.ptr);
        freeMatrix(&newPopulation);
        freeSolutionArr(&popSolutionSet);
        freeSolutionArr(&newSolutionSet);
    }
    freeMatrix(&population);
    freeMatrix(&parents);
    freeMatrix(&offspring);
    free(solutions.ptr);
}