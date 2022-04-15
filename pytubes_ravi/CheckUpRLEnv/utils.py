import random

import torch
import os
import numpy as np
import warnings

DEBUG = True


def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def np2tensor(arrays, device='cpu'):
    tensor = torch.from_numpy(arrays).type(torch.float)
    return tensor.cuda() if device == 'gpu' else tensor


def init(seed):
    warnings.filterwarnings('ignore')
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    torch.multiprocessing.set_start_method("spawn")
    torch.set_default_tensor_type(torch.cuda.FloatTensor)
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)


def mylog(*t, path='./log.txt'):
    t = " ".join([str(now) for now in t])
    print(t)
    if os.path.isfile(path) == False:
        f = open(path, "w+")
    else:
        f = open(path, "a")
    f.write(t + "\n")
    f.close()
