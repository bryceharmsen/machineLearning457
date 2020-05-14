#include <stdlib.h>
#include <math.h>
#include "../SFMT1.5.1/SFMT.h"
#include "arrMtx.h"
#include "randMT.h"

/**
 * Generates a Mersenne-Twister random double and scales the double
 * based on the min and max values.
 * @param min The minimum allowable random value
 * @param max The maximum allowable random value
 * @return The scaled random double
 */
double randNumByRange(range r) {
	double range = r.max - r.min;
	double rand = sfmt_genrand_res53(&sfmt) * range + r.min;
	return rand;
}

/**
 * Selects rands->length number of random values within the range r,
 * ensuring that all values selected are exclusive of each other.
 * @params rands The array to fill with exclusive random values
 * @params r The possible range of values that can be selected
 */
void exclusiveRandsByRange(intArr *rands, range r) {
    int *counterPtr = NULL;
    intArr counter = createEmptyIntArr(counterPtr, (r.max - r.min));
    for (int i = 0; i < rands->length; i++) {
        int randIndex = (int) randNumByRange(r);
        if(counter.ptr[randIndex] == 0) {
            counter.ptr[randIndex] = 1;
            rands->ptr[i] = randIndex;
        } else {
            i--;
        }
    }
}

/**
 * Built for a small range of numbers. Selects rands->length number of
 * random values within the range r, ensuring that all values selected 
 * are exclusive of each other.
 * @param randoms The int array that this methods stores random integers in
 * @param r The range of allowable random values
 * @param excludeVal The value to exclude from the random values, or -1 for
 * 		  no excluded value
 */
void exclusiveRandoms(intArr *randoms, range *r, int excludeVal) {
	int range = (int) (r->max - r->min);
	int *counter = (int *) calloc(range, sizeof(int));
	
	if(excludeVal >= r->min && excludeVal <= r->max) {
		counter[excludeVal] = 1;
	}

	for (int i = 0; i < randoms->length; i++) {
		int random = (int) randNumByRange(*r);
		if (counter[random]) {
			i--;
		} else {
			counter[random] = 1;
			randoms->ptr[i] = random;
		}
	}

	free(counter);
}

/**
 * Fills the given array with random values, based on the min and
 * max range given.
 * @param array The pointer where the array will exist
 * @param length The length of the array
 * @param min The minimum allowable random value
 * @param max The maximum allowable random value
 */
void fillArray(dblArr array, range r) {
	for (int i = 0; i < array.length; i++) {
		array.ptr[i] = randNumByRange(r);
	}
}

/**
 * Creates and fills the matrix double pointer with randome doubles within
 * the specified range.
 * @param matrix The double pointer where the matrix will exist
 * @param rows The number of rows in the matrix
 * @param cols The number of columns in the matrix
 * @param min The minimum allowable random value
 * @param max The maximum allowable random value
 */
void fillMatrix(dblMtx *matrix, range r) {	
	for(int i = 0; i < matrix->rows; i++) {
		for(int j = 0; j < matrix->cols; j++) {
			matrix->ptr[i][j] = randNumByRange(r);
		}
	}
}