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

  int **mat;
  int n;

  Individual::Individual(int sizeN){

    n = sizeN;
    int numVal = sizeN * sizeN;
    // create matrix
    mat = new int*[n];
    for(int j = 0; j < n; j++){
      mat[j] = new int[n];
    }
    for(int i = 0; i < n; i++){
      for(int j = 0; j < n; j++){
        mat[i][j] = rand() % numVal + 1;
      }
    }

    fitness = calcFitness();
  }



  Individual::Individual(int** newIndividual){
    this->mat = newIndividual;
    fitness = calcFitness();
  }


  Individual Individual::makeBabies(Individual other){


    // Initialize child
    int **child;
    child = new int*[n];
    for(int i = 0; i < n; i++){
      child[i] = new int[n];
    }

    // Loop over, randomly picking between either parents to insert generated
    for(int i = 0; i < n; i++){
      for(int j = 0; j < n; j++){
        // pick random probability of which parent inserts a gene
        int randVal = rand() % 100;

        // if less than 50% then insert gene from parent one
        if(randVal <= 50){
          child[i][j] = mat[i][j];
        }else{
          // Insert from parent two
          child[i][j] = other.mat[i][j];
        }

      }
    }

    // Return a new individual AKA the offspring
    return Individual(child);
  }

  float Individual::calcFitness(){

    fitness = 0;
    int size = (n + n) + 2;
    int allSums[size];


    // For calculating the deviation
    float sum, mean, variance, deviation;
    sum = 0;
    mean = 0;
    variance = 0;
    deviation = 0;

    for(int i = 0; i < size; i++){
      allSums[i] = 0;
    }

    // sum rows
    int k = 0;
    for(int i = 0; i < n; i++){
      for(int j = 0; j < n; j++){
        allSums[k] += mat[i][j];
      }
      k++;
    }

    // sum columns
    for(int i = 0; i < n; i++){
      for(int j = 0; j < n; j++){
        allSums[k] += mat[j][i];
      }
      k++;
    }

    // prime diagonalSum
    for(int i = 0; i < n; i++){
      allSums[k] += mat[i][i];
    }
    k++;

    // secondary diagonal sum
   for(int i = 0; i < n; i++){
     allSums[k] += mat[i][n-1-i];
   }


   // Find the mean
   for(int i = 0; i < size; ++i){
     sum += allSums[i];
   }
   mean = sum/size;

   // find the variance
   for(int i = 0; i < size; ++i){
     variance += pow(allSums[i]-mean, 2);
   }
   variance = variance/size;

   // find deviation and store it in fitness
   deviation = sqrt(variance);
   fitness = deviation;

   return fitness;

  }
