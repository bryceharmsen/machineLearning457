#ifndef DBL_ARR_MTX
#define DBL_ARR_MTX

/*Structures for Arrays and Matrices*/

typedef struct intArr {
    int* ptr;
    int length;
} intArr;

typedef struct dblArr {
    double* ptr;
    int length;
} dblArr;


typedef struct dblMtx {
    double** ptr;
    int rows;
    int cols;
} dblMtx;

/*Functions for Arrays and Matrices*/

intArr createEmptyIntArr(int *ptr, int length);
dblArr createEmptyArray(double *ptr, int length);
dblArr copyArray(dblArr *original, double *copyPtr);
double sum(dblArr *values);
void copyMatrix(dblMtx *original, dblMtx *copy);
void copyPtr(double *original, double *copy, int length);
void swapMtxPtr(double **matrixA, double **matrixB);
dblMtx createEmptyMatrix(double **ptr, int rows, int cols);
void freeMatrix(dblMtx *matrix);

#endif