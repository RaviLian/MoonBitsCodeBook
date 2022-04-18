import math

import numpy as np

# 常规检查项目及平均服务时间
# process_times = [3, 3, 4, 2, 3, 2, 5, 6]
process_times = [3, 2, 6]  # 简化版检查项目or科室，假设仅有一个科室，不区分性别
POP_SIZE = 10  # 种群大小
CROSS_RATE = 0.8  # 交叉率
MUTATION_RATE = 1.0  # 变异率
N_GENERATIONS = 100  # 迭代次数
T_W = 5  # 惩罚成本参数
BATCH_SIZE = 5  # 每30分钟一批人
TOTAL_SIZE = 10  # 2批；早7:00--11:00 240分钟，8批 TODO: 不足每批次人数的补0

"""
按批次给染色体分段，同一批次的才能进行变异
"""


class HybridGeneticAlgo:
    def __init__(self, total_size, cross_rate, mutation_rate, pop_size, p_time, batch_size):
        self.total_size = total_size  # 一共多少人
        self.batch_bound = [1, len(p_time) * batch_size + 1]  # 每批人检查项目编码的界限
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        self.process = p_time  # 项目处理时间
        self.batch_size = batch_size  # 每批人数
        self.DNA_batch_size = self.batch_size * len(self.process)  # 每批人的项目编码维度
        self.DNA_size = self.total_size // self.batch_size * self.DNA_batch_size  # 所有人综合的项目编码维度
        self.batch_count = math.ceil(self.total_size / self.batch_size)

        self.seq = [i for i in range(self.batch_bound[0], self.batch_bound[1])]
        """DNA生成1-15随机数，按行拼接"""
        # self.dna = self.gen_dna()
        """种群随机生成，把dna按列拼接"""
        self.pop = self.gen_pop()

    def gen_dna(self):
        loop_count = self.DNA_size // self.DNA_batch_size
        dna = np.random.choice(self.seq, self.DNA_batch_size, replace=False)
        dna = dna.reshape(1, self.DNA_batch_size)
        for i in range(1, loop_count):
            tmp = np.random.choice(self.seq, self.DNA_batch_size, replace=False)
            tmp += i * 15
            tmp = tmp.reshape(1, self.DNA_batch_size)
            dna = np.vstack((dna, tmp))
        return dna

    def gen_pop(self):
        pop = self.gen_dna()
        for i in range(1, self.pop_size):
            pop = np.vstack((pop, self.gen_dna()))
        pop = pop.reshape(self.pop_size, self.batch_count, self.DNA_batch_size)
        return pop




if __name__ == '__main__':
    hga = HybridGeneticAlgo(TOTAL_SIZE, CROSS_RATE, MUTATION_RATE, POP_SIZE, process_times, BATCH_SIZE)
    print(hga.pop)
    print(hga.pop.shape)  # (10, 2, 15)
