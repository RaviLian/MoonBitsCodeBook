import numpy as np


POP_SIZE = 100
DNA_SIZE = 10
X_BOUND = [0, 5]
pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
# float(2 ** DNA_SIZE - 1 = 1023
# 2 ** np.arange(DNA_SIZE)[::-1] = [2^9 - 2^0]
# [2^p - 2^0 除以 1023] (2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1)
a = (2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1)
print(pop[0])
print(a)
print(np.dot(pop[0], a) * X_BOUND[1])
print()
print(pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1))