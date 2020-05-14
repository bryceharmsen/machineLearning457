#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>
#include "fileIO.h" ////////DELETE///////////
#include "arrMtx.h"
#include "benchmarks.h"

#define sq(A)		((A) * (A)) 		/* Square x */

#define sumSq(A,B)	(sq(A) + sq(B)) 	/* Sum of Squares */

#define rtabs(A)	sqrt(fabs(A)) 	/* Square Root of Abs Value */

//===1===
/**
 * Calculates the output of one component in the Schwefel summation.
 * @param x A particular function input
 * @return The summation component result
 */
double schweSum(double x) {
	return -x * sin(rtabs(x));
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double schwefel(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length; i++) {
		sum += schweSum(x->ptr[i]);
	}
	
	return 418.9829*x->length - sum;
}
//===2===

/**
 * A benchmark function, 1st DeJong's, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double deJong1(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length; i++) {
		sum += sq(x->ptr[i]);
	}
	
	return sum;
}
//===3===
/**
 * Calculates the output of one component in the Rosenbrock summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double roseSum(double x0, double x1) {
	return 100*sq(sq(x0) - x1) + sq(1 - x0);
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double rosenbrock(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += roseSum(x->ptr[i], x->ptr[i+1]);
	}
	
	return sum;
}
//===4===
/**
 * Calculates the output of one component in the Rastrigin summation.
 * @param x A particular function input
 * @return The summation component result
 */
double rastSum(double x) {
	return sq(x) - 10*cos(2*M_PI*x);
}


/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double rastrigin(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length; i++) {
		sum += rastSum(x->ptr[i]);
	}
	
	return 10 * x->length * sum;
}
//===5===
/**
 * Calculates the output of one component in the Griewangk summation.
 * @param x A particular function input
 * @return The summation component result
 */
double griewSum(double x) {
	return sq(x) / 4000.0;
}


/**
 * Calculates the output of one component in the Griewangk product.
 * @param x A particular function input
 * @param i The current component index
 * @return The product component result
 */
double griewProd(double x, int i) {
	return cos(x / sqrt(i));
}


/**
 * A benchmark function, which relies on the sum and product of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double griewangk(dblArr *x) {
	double sum = 0;
	double prod = 1;
	for (int i = 0; i < x->length - 1; i++) {
		sum += griewSum(x->ptr[i]);
		prod *= griewProd(x->ptr[i], i + 1);
	}
	return 1 + sum - prod;
}
//===6===
/**
 * Calculates the output of one component in the Envelope Sine Wave summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double envSinSum(double x0, double x1) {
	return 0.5 + sin(sq(sumSq(x0,x1) - 0.5)) / sumSq(1, 0.001*sumSq(x0,x1));
}

/**
 * A benchmark function, Envelope Sine Wave, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double envSine(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += envSinSum(x->ptr[i], x->ptr[i+1]);
	}
	
	return -sum;
}
//===7===
/**
 * Calculates the output of one component in the Stretch V Sine Wave summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double vSinSum(double x0, double x1) {
	return pow(sumSq(x0,x1), 0.25) * sin(sq(50*pow(sumSq(x0,x1),0.1))) + 1;
}

/**
 * A benchmark function, Stretch V Sine Wave, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double stretchVSine(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += vSinSum(x->ptr[i], x->ptr[i+1]);
	}
	
	return sum;
}
//===8===
/**
 * Calculates the output of one component in the Ackley's 1 summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double ack1Sum(double x0, double x1) {
	return 1/pow(M_E, 0.2) * sqrt(sumSq(x0,x1)) + 3*(cos(2*x0) + sin(2*x1));
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double ackleys1(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += ack1Sum(x->ptr[i], x->ptr[i+1]);
	}
	
	return sum;
}
//===9===
/**
 * Calculates the output of one component in the Ackley's 2 summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double ack2Sum(double x0, double x1) {
	return 20 + M_E - 20/pow(M_E, 0.2*sqrt(sumSq(x0,x1)/2.0)) - pow(M_E, 0.5*(cos(2*M_PI*x0) + cos(2*M_PI*x1)));
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double ackleys2(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += ack2Sum(x->ptr[i], x->ptr[i+1]);
	}
	
	return sum;
}
//==10===
/**
 * Calculates the output of one component in the Egg Holder summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double eggSum(double x0, double x1) {
	return -x0*sin(rtabs(x0 - x1 - 47)) - (x1 + 47)*sin(rtabs(x1 + 47 + x0/2.0));
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double eggHolder(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += eggSum(x->ptr[i], x->ptr[i+1]);
	}
	
	return sum;
}
/**
 * Calculates the output of one component in the Rana summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double ranaSum(double x0, double x1) {
	double sum = rtabs(x1 + x0 + 1);
	double diff = rtabs(x1 - x0 + 1);
	
	return x0*sin(diff)*cos(sum) + (x1 + 1)*cos(diff)*sin(sum);
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double rana(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += ranaSum(x->ptr[i], x->ptr[i+1]);
	}
	
	return sum;
}
//==12===
/**
 * Calculates the output of one component in the Pathological summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double pathSum(double x0, double x1) {
	return 0.5 + (sin(sq(100*sq(x0) + sq(x1))) - 0.5) / (1 + 0.001*sq(sumSq(x0,x1) - 2*x0*x1));
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double pathological(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += pathSum(x->ptr[i], x->ptr[i+1]);
	}
	
	return sum;
}
//==13===
/**
 * Calculates the output of one component in the Michalewicz summation.
 * @param x A particular function input
 * @param i The current component index
 * @return The summation component result
 */
double michaSum(double x, int i) {
	return sin(x) * pow(sin(i * sq(x) / M_PI), 20);
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double michalewicz(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length; i++) {
		sum += michaSum(x->ptr[i], i + 1);
	}
	
	return -sum;
}
//==14===
/**
 * Calculates the output of one component in the Masters Cosine summation.
 * @param x0 The function input x_i
 * @param x1 The function input x_i+1
 * @return The summation component result
 */
double mCosSum(double x0, double x1) {
	return pow(M_E, -(sumSq(x0,x1) + 0.5*x1*x0)/8.0) * cos(4*sqrt(sumSq(x0,x1) + 0.5*x0*x1));
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double mastersCos(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length - 1; i++) {
		sum += mCosSum(x->ptr[i], x->ptr[i+1]);
	}
	
	return -sum;
}
//==15===
/**
 * Calculates the output of one component in the Quartic summation.
 * @param x A particular function input
 * @param i The current component index
 * @return The summation component result
 */
double quartSum(double x, int i) {
	return i * pow(x, 4);
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double quartic(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length; i++) {
		sum += quartSum(x->ptr[i], i + 1);
	}
	
	return sum;
}
//==16===
/**
 * Calculates the output of one component in the Levy summation.
 * @param x A particular function input
 * @param wN 1 + (x - 1)/4, an expression dependent on x
 * @return
 */
double levySum(double x, double wN) {
	double w = 1 + (x - 1)/4;
	return sq(w - 1)*(1 + 10*sq(sin(M_PI*w + 1))) + sq(wN - 1)*(1 + sq(sin(2*M_PI*wN)));
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double levy(dblArr *x) {
	double sum = sq(sin(M_PI*(1 + (x->ptr[0] - 1)/4.0)));
	double wN = 1 + (x->ptr[x->length] - 1)/4;
	for (int i = 0; i < x->length - 1; i++) {
		sum += levySum(x->ptr[i], wN);
	}
	
	return sum;
}
//==17===
/**
 * Calculates the output of one component in the Step summation.
 * @param x A particular function input
 * @return The summation component result
 */
double stepSum(double x) {
	return sq(fabs(x) + 0.5);
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double step(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length; i++) {
		sum += stepSum(x->ptr[i]);
	}
	
	return sum;
}
//==18===
/**
 * Calculates the output of one component in the Alpine summation.
 * @param x A particular function input
 * @return The summation component result
 */
double alpSum(double x) {
	return fabs(x*sin(x) + 0.1*x);
}

/**
 * A benchmark function, which relies on the summation of expressions.
 * @param x The inputs to the function
 * @param n The number of function inputs
 * @return the function solution
 */
double alpine(dblArr *x) {
	double sum = 0;
	for (int i = 0; i < x->length; i++) {
		sum += alpSum(x->ptr[i]);
	}
	
	return sum;
}
//=end===

/**
 * Provided an array of inputs, the number of inputs and the function ID,
 * this function selector will call the identified function with the input array.
 * @param x The input array
 * @param n The dimension of the inputs
 * @param id The function ID
 * @return The function solution
 */
double functionSelector(dblArr *x, int id) {
	double solution;
	switch (id) {
		case 1:
			solution = schwefel(x);
			break;
		case 2:
			solution = deJong1(x);
			break;
		case 3:
			solution = rosenbrock(x);
			break;
		case 4:
			solution = rastrigin(x);
			break;
		case 5:
			solution = griewangk(x);
			break;
		case 6:
			solution = envSine(x);
			break;
		case 7:
			solution = stretchVSine(x);
			break;
		case 8:
			solution = ackleys1(x);
			break;
		case 9:
			solution = ackleys2(x);
			break;
		case 10:
			solution = eggHolder(x);
			break;
		case 11:
			solution = rana(x);
			break;
		case 12:
			solution = pathological(x);
			break;
		case 13:
			solution = michalewicz(x);
			break;
		case 14:
			solution = mastersCos(x);
			break;
		case 15:
			solution = quartic(x);
			break;
		case 16:
			solution = levy(x);
			break;
		case 17:
			solution = step(x);
			break;
		case 18:
			solution = alpine(x);
			break;
		default:
			printf("ERR: Unassigned function value.");
			return 0;
			break;
	}
	return solution;
}

/**
 * Returns the index of the best solution in the set of solutions provided
 * @param solutions The solutions to search through of the most optimal solution
 */
int findBestSolution(dblArr *solutions) {
	double best = DBL_MAX;
	int bestIndex = 0;
	double current = 0;
	//printf("New Solution Set: \n");
	for (int i = 0; i < solutions->length; i++) {
		current = solutions->ptr[i];
		//printf("[%d,%lf],", i, current);
		if (current < best) {
			best = current;
			bestIndex = i;
		}
	}
	//printf("\n\n");
	return bestIndex;
}

/**
 * Gets the indices of the subset of solutions with the most optimal fitness value. The size of the
 * bestIndices array determines the size of the subset.
 * @param solutionsOriginal The original solutions to search through
 * @param selectedSolutions The indices of the solutions that are to make up the universal set
 * @param bestIndices The empty array that will be filled with the indices of the most optimal fitnesses
 */
void getBestSolutionSubset(dblArr *solutionsOriginal, intArr *selectedSolutions, intArr *bestIndices) {
	double *solutionsPtr = NULL;
	dblArr solutions = copyArray(solutionsOriginal, solutionsPtr);
	for (int b = 0; b < bestIndices->length; b++) { //for each best index
		double best = DBL_MAX;
		int bestIndex = 0;
		for (int i = 0; i < selectedSolutions->length; i++) { //go through all selected indices
			int selectedIndex = selectedSolutions->ptr[i];
			if (solutions.ptr[selectedIndex] < best) { //if current sol'n beats best
				best = solutions.ptr[selectedIndex];
				bestIndex = selectedIndex;
			}
		}
		bestIndices->ptr[b] = bestIndex;
		solutions.ptr[bestIndex] = DBL_MAX;
	}
}

/**
 * Finds the fitness for each vector in the provided population and places these fitnesses
 * in the provided solutions array.
 * @param solutions The empty solutions dblArr to be filled with population fitnesses
 * @param population The population of vectors to be evaluated
 * @param functionID The ID of the benchmark function
 */
void populationBulkSolve(dblArr *solutions, dblMtx *population, int functionID) {
	for (int row = 0; row < population->rows; row++) {
		dblArr x = {population->ptr[row], population->cols};
		solutions->ptr[row] = functionSelector(&x, functionID);
	}
}

/**
 * Creates a solution based on the vector provided and the determined benchmark function
 * @param x The vector inputs to be provided to the function
 * @param functionID The ID of the benchmark function
 */
solution createSolution(dblArr *x, int functionID) {
	double fitness = functionSelector(x, functionID);
	solution sln = {{x->ptr, x->length}, fitness};
	return sln;
}

/**
 * Converts the provided population and solutions into an array of solution-type structs.
 * @param pairsPtr The empty array to be filled with solutions
 * @param population The population to be included in the solution array
 * @pram solutions The respective solutions to be assigned to the populations in the
 * solution array
 */
solutionArr convertToSolutions(solution *pairsPtr, dblMtx *population, dblArr *solutions) {
	pairsPtr = (solution *) malloc(population->rows * sizeof(solution));
	solutionArr pairs = {pairsPtr, population->rows};
	for (int sln = 0; sln < pairs.rows; sln++) {
		double *solutionInputPtr = (double *) calloc(population->cols, sizeof(double));
		copyPtr(population->ptr[sln], solutionInputPtr, population->cols);
		dblArr solutionInput = {solutionInputPtr, population->cols};
		solution current = {solutionInput, solutions->ptr[sln]};
		pairs.ptr[sln] = current;
	}
	return pairs;
}

/**
 * Frees the alloted memory of a solutionArr
 * @param solutions The solutionArr to free
 */
void freeSolutionArr(solutionArr * solutions) {
	for (int i = 0; i < solutions->rows; i++) {
		free(solutions->ptr[i].input.ptr);
	}
	free(solutions->ptr);
}

/**
 * Allocates memory for a new solution, then makes a copy of the
 * provided solution.
 * @param original The original solution
 * @return The copy of the original solution with memory allocated
 * for the pointer
 */
solution copySolution(solution *original, double *inputPtr) {
	solution copy = {copyArray(&(original->input), inputPtr), original->fitness};
	return copy;
}

/**
 * Frees the allocated memory provided when the solution was
 * created.
 * @param sln The solution containing memory to free
 */
void freeSolution(solution *sln) {
	free(sln->input.ptr);
}