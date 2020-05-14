#include <stdlib.h>
#include <stdio.h>
#include "arrMtx.h"


intArr createEmptyIntArr(int *ptr, int length) {
    ptr = (int *) calloc(length, sizeof(int));
    intArr array = {ptr, length};
    return array;
}

/**
 * createEmptyArray uses calloc to allocate memory to the given
 * pointer of type double with the given length. The function also assigns
 * the given length to the length field of the dblArr structure.
 * @param ptr The given pointer to an array of doubles
 * @param length The given length of the double array
 * @return The dblArr structure containing properly allocated
 *         double pointer and a field holding the proper length of the array
 */
dblArr createEmptyArray(double *ptr, int length) {
    ptr = (double *) calloc(length, sizeof(double));
    dblArr array = {ptr, length};
    return array;
}

/**
 * Allocates memory for a dblArray struct and copies
 * the dblArr contents into it, then returns the new
 * dblArr.
 * @param original The original array
 * @return The array the doubles and length value were
 * copied to
 */
dblArr copyArray(dblArr *original, double *copyPtr) {
    dblArr copy = createEmptyArray(copyPtr, original->length);
    for (int i = 0; i < original->length; i++) {
        copy.ptr[i] = original->ptr[i];
    }
    return copy;
}

/**
 * sum adds up all of the values provided in the dblArr
 * @param values The values to sum
 */
double sum(dblArr *values) {
    double sum = 0;
    for (int i = 0; i < values->length; i++) {
        sum += values->ptr[i];
    }
    return sum;
}

/**
 * Copies pointer contents of type double from one pointer
 * to another of the same size.
 * @param original The original pointer
 * @param copy The pointer to copy the doubles to
 * @param length The length of both pointers
 */
void copyPtr(double *original, double *copy, int length) {
    for (int i = 0; i < length; i++) {
        copy[i] = original[i];
    }
}

void copyMatrix(dblMtx *original, dblMtx *copy) {
    if (original->rows != copy->rows || original->cols != copy->cols) {
        fprintf(stderr, "ERROR: Incompatible matrix sizes in copyMatrix().\n");
        return;
    }
    for (int i = 0; i < original->rows; i++) {
        for (int j = 0; j < original->cols; j++) {
            copy->ptr[i][j] = original->ptr[i][j];
        }
    }
}

void swapMtxPtr(double **matrixA, double **matrixB) {
    double **tempPtr = matrixA;
    matrixA = matrixB;
    matrixB = tempPtr;
}

/**
 * Creates an empty matrix at the given pointer based on dimensions given
 * @param ptr The double pointer of type double where the memory will be
 * allocated and initialized
 * @param rows The number of rows to allocate for the matrix
 * @param cols The number of columns to allocate for the matrix
 * @return The dblMtx structure with memory allocated to the double pointer
 * and the rows and columns defined in the structure
 */
dblMtx createEmptyMatrix(double **ptr, int rows, int cols) {
    ptr = (double**) malloc(rows * sizeof(double *));
    for (int i = 0; i < rows; i++) {
		ptr[i] = (double *) calloc(cols, sizeof(double));
	}
    dblMtx matrix = {ptr, rows, cols};
    return matrix;
}

/**
 * De-allocates (frees) the memory at the given double pointer.
 * @param matrix The double pointer memory to free
 * @param rows The number of rows in the matrix
 */
void freeMatrix(dblMtx *matrix) {
	for (int i = 0; i < matrix->rows; i++) {
		free(matrix->ptr[i]);
	}
    free(matrix->ptr);
}