#ifndef RAND_MT
#define RAND_MT

#include "../SFMT1.5.1/SFMT.h"
#include "arrMtx.h"
sfmt_t sfmt;

/*Structures from randMT*/
typedef struct range {
    double min;
    double max;
} range;

/*Functions from randMT*/

double randNumByRange(range r);
void exclusiveRandoms(intArr *randoms, range *r, int excludeVal);
void fillArray(dblArr array, range r);
void fillMatrix(dblMtx *matrix, range r);

#endif