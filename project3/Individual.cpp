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
#include <cmath>
#include "Individual.h"

using namespace std;


//class Individual {

  float fitness = 0;
  int **mat;
  int n;


  Individual::Individual(){

    cout << "Individual made" << endl;
    // create matrix
    mat = new int*[3];
    for(int j = 0; j < 3; j++){
      mat[j] = new int[3];
    }
    srand(time(NULL));
    for(int i = 0; i < 3; i++){
      for(int j = 0; j < 3; j++){
        mat[i][j] = rand() % 10;
      }
    }

    fitness = calcFitness();
  }

  Individual::Individual(int** newIndividual){
    this->mat = newIndividual;
    fitness = calcFitness();
  }

  // Destructor
  //Individual::~Individual(){
    //delete []mat;
  //}


  Individual Individual::makeBabies(Individual other){

    cout << "Making babies" << endl;

    // Initialize child
    int **child;
    child = new int*[3];
    for(int i = 0; i < 3; i++){
      child[i] = new int[3];
    }
    cout << "Child created" << endl;

    // Loop over, randomly picking between either parents to insert generated
    for(int i = 0; i < 3; i++){
      for(int j = 0; j < 3; j++){
        // pick random probability of which parent inserts a gene
        int randVal = rand() % 100;
        float p = randVal / 100;
        cout << "Random value assigined" << endl;

        // if less than 50% then insert gene from parent one
        if(p <= 0.50){
          child[i][j] = mat[i][j];
          cout << "Probability less than" << endl;
        }else{
          // Insert from parent two
          cout << "Inserting from parent two" << endl;
          child[i][j] = other.mat[i][j];
        }
        cout << "P: " << p << endl;

      }
    }
    cout << "returning new child" << endl;
    // Return a new individual AKA the offspring
    return Individual(child);
  }

  float Individual::calcFitness(){

    cout << "Calculating fitness" << endl;
    int rowSum[3];
    int columnSum[3];
    int diagonalSum[2];
    int allSums[8];

    // For calculating the deviation
    float sum, mean, variance, deviation;

    // sum rows
    int k = 0;
    for(int i = 0; i < 3; i++){
      for(int j = 0; j < 3; j++){
        //rowSum[k] += mat[i][j];
        allSums[k] += mat[i][j];
      }
      k++;
    }

    // sum columns
    //k = 0;
    for(int i = 0; i < 3; i++){
      for(int j = 0; j < 3; j++){
        //columnSum[k] += mat[j][i];
        allSums[k] += mat[j][i];
      }
      k++;
    }

    // prime diagonalSum
    for(int i = 0; i < 3; i++){
      diagonalSum[0] += mat[i][i];
      allSums[k] += mat[i][i];
    }
    k++;

    // secondary diagonal sum
   for(int i = 0; i < 3; i++){
     diagonalSum[1] += mat[i][3-1-i];
     allSums[k] += mat[i][3-1-i];
   }

   // Find the mean
   for(int i = 0; i < 8; i++){
     sum += allSums[i];
   }
   mean = sum/8;

   // find the variance
   for(int i = 0; i < 8; i++){
     variance += pow(allSums[i]-mean, 2);
   }
   variance = variance/8;

   // find deviation and store it in fitness
   deviation = sqrt(variance);
   fitness = deviation;

   return fitness;

  }


//};
