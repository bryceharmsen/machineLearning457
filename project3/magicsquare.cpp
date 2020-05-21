#include <iostream>
#include <thread>
#include <stdlib.h>
#include <unistd.h>
#include <bits/stdc++.h>
#include <pthread.h>
#include <stdio.h>
#include <random>
#include <mutex>
#include <cstdlib>
#include <sys/types.h>
#include <sys/syscall.h>
#include <time.h>

#include "Individual.h"

using namespace std;


void selection(){

}

void crossover(){

}

bool operator<(const Individual &ind1, const Individual &ind2){
  cout << "Comparing" << endl;
  return ind1.fitness < ind2.fitness;
}

int main(){

  int popSize = 10;
  int n = 3;
  srand(time(NULL));

  int currentGen = 0;
  bool found = false;

  vector<Individual> population;
  //Individual population[popSize];
  //int m = sizeof(population)/sizeof(population[0].fitness);

  // create the population
  for(int i = 0; i < popSize; i++){
    Individual individual;
    population.push_back(individual);
  }

  while(!found){

    // sort the population by fitness score
    sort(population.begin(), population.end());

    cout << "Population sorted" << endl;

    if(population[0].fitness <= 0){
      found = true;
      break;
    }

    vector<Individual> newGen;

    // 10% of fittest population goes to next generation
    int s = (10*popSize)/100;
    for(int i = 0; i < s; i++){
      newGen.push_back(population[i]);
    }
    cout << "10% move on" << endl;

    // 50% of fittest will mate and make offspring
    s = (90*popSize) / 100;
    for(int i = 0; i<s; i++){
      int len = population.size();
      int r = rand() % 50;
      cout << "random number 1: " << r << endl;
      Individual parent1 = population[r];
      cout << "Parent 1 selected" << endl;
      r = rand() % 50;
      cout << "random number 2: " << r << endl;
      Individual parent2 = population[r];
      Individual offspring = parent1.makeBabies(parent2);
      newGen.push_back(offspring);
      cout << "Offspring created" << endl;
    }
    population = newGen;
    cout << "Generation: " << currentGen << "\t";
    cout << "Fitness: " << population[0].fitness << "\n";
    currentGen++;

  }



}
