"""
单种群遗传算法
染色体chromosome:
"""
from collections import deque
import numpy as np

class PatientRecords:
    def __init__(self, total_num):
        self.total = total_num
        self.store = self.__init_store()

    def __init_store(self):
        # 舍弃0位置,不保存
        store = [deque() for _ in range(self.total + 1)]
        return store

    def add_record(self, pidx, record):
        self.store[pidx].append(record)

class ServiceRecords:
    def __init__(self, total_num, serve_times):
        """
        :param total_num: 科室数目
        :param serve_times: 一个列表，保存平均服务时间; 或者一个矩阵，保存所有客户所有项目的服务时间
        """
        self.total = total_num
        self.serve_times = serve_times
        self.store = self.__init_store()

    def __init_store(self):
        # 舍弃0位置,不保存
        store = [deque() for _ in range(self.total + 1)]
        return store

    def add_record(self, service_idx, record):
        """
        :param service_idx: 服务台编号
        :param record: [客户index, 开始检查时间, 结束检查时间]
        """
        self.store[service_idx].append(record)


class DNA:
    def __init__(self, people_num, service_times):
        self.bound = people_num * len(service_times)
        self.patient_records = PatientRecords(people_num)
        self.service_records = ServiceRecords(len(service_times), service_times)
        self.fitness = 0  # 适应度值
        self.result = self.__init_dna()

    def __init_dna(self):
        return np.random.choice([i for i in range(1, self.bound + 1)], size=self.bound, replace=False)


def get_fitness_val(dna):
    """
    计算当前解的适应度值
    """
    pass



if __name__ == '__main__':
    POPULATION_SIZE = 150  # 种群大小, 即解的个数
    N_GENERATIONS = 600    # 迭代次数
    CROSS_RATE = 0.8       # 交叉概率
    MUTATE_RATE = 1.0      # 变异概率
    FIXED_SERVICE_TIMES = [
        3,  # 1体质测试
        3,  # 2内科
        4,  # 3外科
        2,  # 4眼耳口鼻科
        3,  # 5验血
        2,  # 6心电图
        5,  # 7X光
        6,  # 8B超
    ]       # 共28分钟
    TOTAL_PEOPLE_NUM = 40

    d = DNA(TOTAL_PEOPLE_NUM, FIXED_SERVICE_TIMES)
    print(d.result)


