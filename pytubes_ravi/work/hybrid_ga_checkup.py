import math
import sys

import numpy as np

# 常规检查项目及平均服务时间
# process_times = [3, 3, 4, 2, 3, 2, 5, 6]
process_times = [3, 2, 6]  # 简化版检查项目or科室，假设仅有一个科室，不区分性别
POP_SIZE = 10  # 种群大小
CROSS_RATE = 0.8  # 交叉率
MUTATION_RATE = 1.0  # 变异率
N_GENERATIONS = 100  # 迭代次数
T_W = 5  # 惩罚成本参数
BATCH_SIZE = 2  # 每30分钟一批人
TOTAL_SIZE = 4  # 2批；早7:00--11:00 240分钟，8批 TODO: 不足每批次人数的补0

"""
按批次给染色体分段，同一批次的才能进行变异
实现过程：
染色体解码逻辑 translate_DNA =>
适应度打分get_fitness => 挑选优秀子代select => 
染色体交叉crossover => 子代染色体变异mutate => 
整体进化过程evolve:
    def evolve(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:  # for every parent
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop  
"""


class HybridGeneticAlgo:
    def __init__(self, total_size, cross_rate, mutation_rate, pop_size, p_time, batch_size):
        self.total_size = total_size  # 一共多少人
        self.batch_bound = [1, len(p_time) * batch_size + 1]  # 每批人检查项目编码的界限
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        self.process = p_time  # 项目处理时间
        self.room_len = len(self.process)
        self.batch_size = batch_size  # 每批人数
        self.DNA_batch_size = self.batch_size * self.room_len  # 每批人的项目编码维度
        self.DNA_size = self.total_size // self.batch_size * self.DNA_batch_size  # 所有人综合的项目编码维度
        self.batch_count = math.ceil(self.total_size / self.batch_size)

        self.seq = [i for i in range(self.batch_bound[0], self.batch_bound[1])]
        """DNA生成1-15随机数，按行拼接"""
        # self.dna = self.gen_dna()
        """种群随机生成，把dna按列拼接"""
        self.pop = self.gen_pop()

        """客户记录表"""
        self.customer_records = [[] for _ in range(self.total_size)]
        """科室记录表"""
        self.room_records = [[] for _ in range(self.room_len)]

    def gen_dna(self):
        loop_count = self.DNA_size // self.DNA_batch_size
        dna = np.random.choice(self.seq, self.DNA_batch_size, replace=False)
        for i in range(1, loop_count):
            tmp = np.random.choice(self.seq, self.DNA_batch_size, replace=False)
            dna = np.hstack((dna, tmp))
        return dna

    def gen_pop(self):
        pop = self.gen_dna()
        for i in range(1, self.pop_size):
            pop = np.vstack((pop, self.gen_dna()))
        return pop

    def translate_DNA(self, pop):
        # TODO: 整个种群的记录，需要再扩一级
        pop = pop.reshape(self.pop_size, self.batch_count, self.DNA_batch_size)
        dna = pop[0]
        batch = dna[0]
        print(batch)
        for seq in batch:
            if seq <= self.room_len:
                customer_idx = 0
                room_idx = seq - 1
            elif (seq - self.room_len) % self.room_len == 0:
                customer_idx = seq // self.room_len - 1
                room_idx = self.room_len - 1
            else:
                count = seq // self.room_len
                seq = seq - count * self.room_len
                customer_idx = count
                room_idx = seq - 1
            print(customer_idx)
            print(room_idx)
            start_time = self.compute_start_time(customer_idx, room_idx)
            end_time = start_time + self.process[room_idx]
            # 插入合法记录
            self.customer_records[customer_idx].append([room_idx, start_time, end_time])
            self.room_records[room_idx].append([customer_idx, start_time, end_time])
            break
        print(self.customer_records)
        print(self.room_records)

    def compute_start_time(self, customer_idx, room_idx):
        # 遍历room j的所有空闲区间 [S_j, E_j]
        spare_time = []
        if len(self.room_records[room_idx]) == 0:
            spare_time = [0, sys.maxsize]
        else:
            spare_time = self.get_room_spare_time()
        start_time = spare_time[0]
        # 遍历customer i的上一条检查记录，找到结束时间， 若无记录则为0
        if len(self.customer_records[customer_idx]) == 0:
            c_i_jm1 = 0
        else:
            c_i_jm1 = self.customer_records[customer_idx][-1][2]
        # 判断 start_time + self.process[room_idx] 是否小于E_j
        # 小于，则返回当前start_time

        # 大于，则开始时间为 room j 最终一条记录的end_time 与 customer i 的上一条end_time
        # start_time = max(L_j, c_i_{j-1})

        return start_time

    def get_room_spare_time(self):
        return []

    def get_fitness(self):
        pass


if __name__ == '__main__':
    hga = HybridGeneticAlgo(TOTAL_SIZE, CROSS_RATE, MUTATION_RATE, POP_SIZE, process_times, BATCH_SIZE)
    hga.translate_DNA(hga.pop)
