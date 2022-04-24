"""
单种群遗传算法
染色体chromosome:
"""
import numpy as np


class PatientRecords:
    def __init__(self, total_num):
        self.total = total_num
        self.store = self.__init_store()

    def __init_store(self):
        # 舍弃0位置,不保存
        store = [[] for _ in range(self.total + 1)]
        return store

    def add_record(self, pidx, record):
        self.store[pidx].append(record)

    def get_last_project_end(self, pidx):
        """得到上一项目的结束时间"""
        records = self.store[pidx]
        records.sort(key=lambda e: e[2])
        return records[-1][2]


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
        store = [[] for _ in range(self.total + 1)]
        return store

    def add_record(self, service_idx, record):
        """
        :param service_idx: 服务台编号
        :param record: [客户index, 开始检查时间, 结束检查时间]
        """
        self.store[service_idx].append(record)

    def get_idle_times(self, service_idx):
        """得到该服务台的空闲时间区间"""
        service = self.store[service_idx]
        idles = []
        if len(service) == 0:
            return idles.append([0, 240])
        service.sort(key=lambda e: e[1])  # 按照开始检查时间排序
        # 检查0时刻和第一个病人到达时是否有空闲——一般没有
        if service[0][1] - 0 > 0:
            idles.append([0, service[0][1]])
        # 中间的空闲区间
        for i in range(1, len(service)):
            second_time = service[i][1]
            first_time = service[i - 1][2]
            if second_time - first_time > 0:
                idles.append([first_time, second_time])
        # 末尾的空闲区间
        if service[-1][2] < 240:
            idles.append([service[-1][2], 240])
        else:  # 假如超时了，设置标记位-1，代表无限长
            idles.append([service[-1][2], -1])

        return idles


class DNA:
    def __init__(self, people_num, service_times):
        self.bound = people_num * len(service_times)
        self.patient_records = PatientRecords(people_num)
        self.service_records = ServiceRecords(len(service_times), service_times)
        self.fitness = 0  # 适应度值
        self.result = self.__init_dna()

    def __init_dna(self):
        return np.random.choice([i for i in range(1, self.bound + 1)], size=self.bound, replace=False)

    def __repr__(self):
        return self.result.__str__()


def get_fitness(patient_records, service_records):
    """
    计算当前解的适应度值
    """
    pass


class SGA:
    def __init__(self, people_num, service_times, cross_rate, mutation_rate, pop_size):
        self.people_num = people_num
        self.service_times = service_times
        self.project_num = len(service_times)
        self.pc = cross_rate
        self.pm = mutation_rate
        self.pop_size = pop_size
        self.pop = self.__init_pop()

    def __init_pop(self):
        pop = []
        for i in range(self.pop_size):
            pop.append(DNA(self.people_num, self.service_times))
        return pop

    def translate(self):
        """解码"""
        for dna in self.pop:
            pass

    def translate_dna(self, dna):
        """单条dna解码，保存状态并计算适应度"""
        pass

    def get2index(self, item):
        """得到编码解码后客户下标和服务台下标"""
        div = item // self.project_num
        mod = item % self.project_num
        if mod == 0:
            pidx = div
            sidx = self.project_num
        else:
            pidx = div + 1
            sidx = mod
        return pidx, sidx

    def select(self):
        """轮盘赌算法选择交叉Dna"""
        pass

    def crossover(self):
        """交叉"""
        pass

    @staticmethod
    def mutation(chromosome):
        """
        基因突变，任意两个基因交换顺序
        :param chromosome: 染色体
        """
        bound = len(chromosome)
        idx1, idx2 = np.random.choice([i for i in range(0, bound)], size=2, replace=False)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]

    def evolve(self, fitness):
        """将交叉变异后的优良染色体引入种群"""
        # pop = self.select(fitness)
        # pop_copy = pop.copy()
        # for parent in pop:  # for every parent
        #     child = self.crossover(parent, pop_copy)
        #     child = self.mutate(child)
        #     parent[:] = child
        # self.pop = pop
        pass


def run(algo, iter_num):
    for generation in iter_num:
        # 解码种群
        # p_status, service_status = algo.translate(algo.pop)
        # 计算适应度值
        # fit = get_fitness(p_status, service_status)
        # 优良染色体假如种群
        # algo.evolve(fit)
        # 拿到适应度值最好的dna
        # 输入或者记录到list——fitness
        pass


if __name__ == '__main__':
    POPULATION_SIZE = 150  # 种群大小, 即解的个数
    N_GENERATIONS = 600  # 迭代次数
    CROSS_RATE = 0.8  # 交叉概率
    MUTATE_RATE = 1.0  # 变异概率
    FIXED_SERVICE_TIMES = [
        3,  # 1体质测试
        3,  # 2内科
        4,  # 3外科
        2,  # 4眼耳口鼻科
        3,  # 5验血
        2,  # 6心电图
        5,  # 7X光
        6,  # 8B超
    ]  # 共28分钟
    TOTAL_PEOPLE_NUM = 40

    params = {
        'people_num': TOTAL_PEOPLE_NUM,
        'service_times': FIXED_SERVICE_TIMES,
        'cross_rate': CROSS_RATE,
        'mutation_rate': MUTATE_RATE,
        'pop_size': POPULATION_SIZE,
    }

    sga = SGA(**params)
