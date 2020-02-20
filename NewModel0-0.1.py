import numpy as np
from psopy import minimize


filename = 'gt_data_10_authors.csv'

# Read from csv and create numpy array.
dataset = np.genfromtxt(filename, delimiter=',')

constraints = (
    {'type': 'ineq', 'fun': lambda x: x[0]-0.01},
    {'type': 'stin', 'fun': lambda x: 0.1 - x[0]}
)

# Because tolerance for strict inequalities is 0.0001,
# I'm generating between 0 and 0.9999 and not 1.0.
# Also, I'm pretty certain that even 100 particles is overkill.
x0 = np.random.uniform(0.01, 0.1, (100, 1))

results = []

# This is Python's string formatting using the method `str.format`.
record = 'Record: {:05d}    fun: {:.6f}    x: {:.4f}    constr: {:.4f}  {:.4f}'

# Iterate over all records.
for i in range(dataset.shape[0]):
    
    # Options must be specified this way because the function modifies the
    # dictionary passed to the parameter `options`.
    result = minimize(
        lambda x, row: -((row[0]**x[0] + row[1]**x[0] + row[2]**x[0] + 0.1*row[3]**x[0] + 0.1*row[4]**x[0])**(1/x[0])), x0, dataset[i],
        constraints, options={
            'g_rate': 1., 'l_rate': 1., 'max_velocity': 4.,
            'stable_iter': 50, 'sttol': 1e-4})

    # Print a nice pretty report line.
    print(record.format(i + 1, result['fun'], result['x'][0],
                        result['cvec'][0, 0], result['cvec'][0, 1]))

    results.append(result)

# I haven't written any code to save the results in a file because I'm not
# sure about the formatting required. Each item in `results` has,
#
#       cvec -- constraint vector for `x`,
#       fun -- the value of the function for `x`,
#       message, status, success -- result of operation,
#       nit -- number of iterations,
#       nsit -- number of stable iterations,
#       x -- the global best value.
