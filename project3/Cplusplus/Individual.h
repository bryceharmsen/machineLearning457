// Individual header file

#include <iostream>

using namespace std;

class Individual {

public:
  float fitness;
  int **mat;
  //int n = 3;
  int n;
  Individual(int sizeN);
  Individual(int **mat);
  Individual makeBabies(Individual other);
  //~Individual();
  float calcFitness();
};
