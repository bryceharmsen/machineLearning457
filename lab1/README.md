## Perceptron
This is the Perceptron project 1 for Dr. Andonie.

# Running the perceptron
Before running, check that the parameters set in params.yaml are set to your preference. Then, to run, call ```python3 project1.py```

# Testing the perceptron
To run the unit tests built for the perceptron, run ```python -m unittest discover```

# Adding supervised learning data
To contribute to the supervised learning data, access **supervisedData.csv**. The format is:  
**A matrix drawing of the letter L or I**  
**The lowercase letter L or I**  
An example for 3x3 I data looks like:  
0,1,0  
0,1,0  
0,1,0  
i  
We also need 5x5 data for L and I. Contributions are welcome.

# Installing package dependencies
In general, any missing packages on the host machine can be installed with ```pip3 install PACKAGE_NAME```  
For this project, the current install list should suffice:  
```pip3 install pyyaml matplotlib numpy```