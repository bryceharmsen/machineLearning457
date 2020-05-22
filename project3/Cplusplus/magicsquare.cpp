#include <iostream>
#include <stdlib.h>
#include <unistd.h>
#include <bits/stdc++.h>
#include <stdio.h>
#include <random>
#include <cstdlib>
#include <sys/types.h>
#include <sys/syscall.h>
#include <time.h>

#include "Individual.h"

using namespace std;


bool operator<(const Individual &ind1, const Individual &ind2){
  return ind1.fitness < ind2.fitness;
}

void runGA(int popSize, int n, int numGenerations){

  srand(time(NULL));
  int halfPop = popSize / 2;

  int currentGen = 0;

  vector<Individual> population;

  // create the population
  for(int i = 0; i < popSize; i++){
    Individual individual(n);
    population.push_back(individual);
  }

  float bestFitGen1 = 0;
  float worstFitGen1 = 0;
  float avgFitGen1 = 0;
  float bestFitGenZ = 0;
  float worstFitGenZ = 0;
  float avgFitGenZ = 0;
  float fitCount = 0;

  while(currentGen < numGenerations){

    float averageFit = 0;
    if(currentGen == 0){
    // sort the population by fitness score
    sort(population.begin(), population.end());
    }

    // get the first gen stats

    if(currentGen == 0){
      bestFitGen1 = population[0].fitness;
      worstFitGen1 = population[popSize - 1].fitness;
      for(int i = 0; i < popSize; i++){
        fitCount += population[i].fitness;
      }
      avgFitGen1 = fitCount / popSize;
    }


    vector<Individual> newGen;


    // 50% of fittest will mate and make offspring
    int s = (50*popSize) / 100;
    for(int i = 0; i<s; i++){
      int r = rand() % s;
      Individual parent1 = population[r];
      r = rand() % s;
      Individual parent2 = population[r];
      Individual offspring = parent1.makeBabies(parent2);
      averageFit += offspring.fitness;
      newGen.push_back(offspring);
    }

    // make newGeneration vector with 50% of the best from previous generation
    vector<Individual> nextGeneration(&population[0], &population[halfPop]);
    // insert the newGeneration (offspring) into the next generation offspring
    nextGeneration.insert(nextGeneration.end(), newGen.begin(), newGen.end());
    // Get the average fitness from the previous generation
    for(int i = 0; i < halfPop; i++){
      averageFit += nextGeneration[i].fitness;
    }
    //population = nextGeneration;
    population.assign(nextGeneration.begin(), nextGeneration.end());

    currentGen++;

    averageFit /= popSize;


    if(currentGen == numGenerations){
      sort(nextGeneration.begin(), nextGeneration.end());
      bestFitGenZ = nextGeneration[0].fitness;
      worstFitGenZ = nextGeneration[popSize - 1].fitness;
      avgFitGenZ = averageFit;
      break;
    }
  }
  cout << "\t\t";
  cout << "Population size: " << popSize << "\t\t" << "Size of matrix: " << n << "\t\t" << "Number of Generations: " << numGenerations << endl;
  cout << "\t\t" << "Generation 1 >>> " << "\t\t" << "Best fitness: " << bestFitGen1 << "\t\t" << "Worst fitness: " << worstFitGen1 <<
  "\t\t" << "Average fitness: "  << avgFitGen1<< "\t\t" << endl;
  cout << "\t\t" << "Last Generation >>> " << "\t\t" << "Best fitness: " << bestFitGenZ << "\t\t\t" << "Worst fitness: "  << worstFitGenZ <<
  "\t\t" << "Average fitness: "  << avgFitGenZ<< "\t\t" << endl;
  cout << endl;



}


int main(){

  int testPopulationSize[] = {100, 1000, 2000};
  int testSizeMatrix[] = {3, 9, 10};
  int testGenerations[] = {2000, 1000, 100};

  //runGA(1000, 4, 1000);


  // same population size, different size matrix and generations
  for(int i = 0; i < 2; i++){
    for(int j = 0; j < 2; j++){
      runGA(testPopulationSize[i], testSizeMatrix[j], testGenerations[j]);
    }
  }

  // same size matrix, different size populations and # of generations
  for(int i = 0; i < 2; i++){
    for(int j = 0; j < 2; j++){
      runGA(testPopulationSize[j], testSizeMatrix[i], testGenerations[j]);
    }
  }

  // same generation number, different size matrix and populationsize
  for(int i = 0; i < 2; i++){
    for(int j = 0; j < 2; j++){
      runGA(testPopulationSize[j], testSizeMatrix[j], testGenerations[i]);
    }
  }
  //*/




}
