"""
测试一些小功能的文件
"""
import random
import numpy as np
from collections import deque


def crossover():
    """
    交叉
    :return:
    """
    P1 = [1, 4, 6, 3, 2, 5]  # 随机选择一个染色体
    P2 = [5, 6, 3, 4, 1, 2]  # 随机选择一个染色体
    # cross_idx = random.randint(1, 2)
    cross_idx = 1 # 随机获取一个顾客的编号
    project_num = 3 # 项目数目
    change_bound = get_project_bound(cross_idx, project_num) # 解码顾客项目编号范围
    # 获取两条染色体上的顾客项目idx和seq
    idx1, seq1 = gen_patient_proj_idx_seq(P1, change_bound)
    idx2, seq2 = gen_patient_proj_idx_seq(P2, change_bound)
    # 根据一定概率pc交叉产生子代C1， C2
    C1 = change_patient(P1.copy(), idx1, seq2)
    C2 = change_patient(P2.copy(), idx2, seq1)
    # 根据一定概率pm子代染色体变异
    mutation(C1)
    mutation(C2)


def get_project_bound(p, m):
    """
    :param p 客户编号 [1, n]
    :param m 检查项目的数目
    """
    start = (p - 1) * m + 1
    end = p * m
    return [i for i in range(start, end + 1)]


def gen_patient_proj_idx_seq(chromosome, bound):
    """
    :param chromosome: 染色体
    :param bound: 顾客项目编码范围
    :return: 两个list，一个是顾客项目编码在染色体中的index，一个是顾客项目编码值
    """
    idx = [i for i in range(len(chromosome)) if chromosome[i] in bound]
    seq = [val for val in chromosome if val in bound]
    return idx, seq


def change_patient(chromosome, own_change_index, other_proj):
    """
    换某一顾客的全部项目
    :param chromosome: 染色体备份-浅拷贝就够用
    :param own_change_index: 自己要更换顾客项目的各个位置index
    :param other_proj: deque结构，要更换的项目，要求保持之前的顺序
    :return: 新的染色体
    """
    for i in range(len(chromosome)):
        if i in own_change_index:
            chromosome[i] = other_proj.pop(0)  # 从左边出队
    return chromosome


def mutation(chromosome):
    """
    基因突变，任意两个基因交换顺序
    :param chromosome: 染色体
    :return:
    """
    bound = len(chromosome)
    idx1, idx2 = np.random.choice([i for i in range(0, bound)], size=2, replace=False)
    chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]



if __name__ == '__main__':
    # crossover()
    a = np.array([1, 2, 3, 4])
    a = list(a)
    s = a.__str__()
    print(s)
