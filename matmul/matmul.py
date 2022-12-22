import numpy as np
from time import time


def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    C = np.matmul(A, B)
    latency = time() - start
    return latency


def main(params):
    n = int(params['n'])
    result = matmul(n)
    print(result)
    return {'latency':result}
