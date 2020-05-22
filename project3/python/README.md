## Python 3 Genetic Algorithm
Included in this package are a few files that implement genetic algorithm and some utility and helper functions to aid the tuning and visualization of the genetic algorithm, or GA.

# Running the code
The driver file for this package is sinln.py. This can be run with the command:
```python3 sinln.py params.yaml```

# Other features of this package
While sinln.py is the driver, the SinLn class inherits from the abstract class GA inside ga.py. The GA class provides an outline for the genetic algorithm, providing a couple of concrete methods that enforce the general process of the genetic algorithm, as well as making a contract with children classes through abstract methods, enforcing the key pieces of the algorithm be implemented for the given problem set. Two other files, plotter.py and util.py, allow for both data visualization and algorithm tuning respectively. The util.py provides a function for processing yaml files. If the user would like to tune the SinLn algorithm, they should do so through params.yaml. Lastly the test_sinln.py provides proof of some level of proper functionality within the SinLn object through unit testing.