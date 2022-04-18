import functools
import time

import numpy as np


def func1():
    seq = [i for i in range(1, 16)]
    a = np.random.choice(seq, 15, replace=False)
    for i in range(3):
        b = np.random.choice(seq, 15, replace=False)
        a = np.row_stack((a, b))
    return a


def func2():
    DNA_size = 40
    DNA_batch_size = 5
    count = DNA_size // DNA_batch_size

    dna = np.random.choice([i for i in range(1, 16)], 15, replace=False)
    for i in range(1, count):
        tmp = np.random.choice([i for i in range(1, 16)], 15, replace=False)
        tmp += i * 15
        dna = np.hstack((dna, tmp))

    print(dna)


def func3():
    print(np.vstack([np.random.permutation(15) + 1 for _ in range(10)]))


def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        fc = fn(*args, **kwargs)  # 执行函数
        t2 = time.time()
        print('%s executed in %s ms' % (fn.__name__, t2 - t1))
        return fc  # 返回值

    return wrapper


def log_info(fn):
    @functools.wraps(fn)
    def wrapper(var_str, var):
        print()
        fc = fn(var_str, var)  # 执行函数
        return fc  # 返回值

    return wrapper


@log_info
def log(var_str, var):
    print(var_str + "==>")
    print(var)


def translateDNA():
    """TSP的DNA解读，仅用于GUI显示内容"""
    DNA_size = 3
    pop_size = 5
    city_position = np.random.rand(DNA_size, 2)  # (3, 2) 生成3个坐标
    log("city_position", city_position)
    pop = np.vstack([np.random.permutation(DNA_size) for _ in range(pop_size)])
    log("pop", pop)
    lx = np.empty_like(pop, dtype=np.float64)
    ly = np.empty_like(pop, dtype=np.float64)
    for i, d in enumerate(pop):
        log("(i, d)", (i, d))
        city_coord = city_position[d]
        lx[i, :] = city_coord[:, 0]
        ly[i, :] = city_coord[:, 1]

    print(lx)
    print(lx.shape)


if __name__ == '__main__':
    pass

