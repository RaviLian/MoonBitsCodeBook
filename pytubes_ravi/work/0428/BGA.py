"""
1. 随机产生初始解，建立初始种群，种群规模为Z；进行解码和适应度计算
2. 使用交叉算子和突变算子对当前种群中对解进行重组，产生后代，形成新的种群。进行解码和适应度计算
3. 迭代：重复1-2，直到解一定代数内最优值没有发生明显改进，输出当前最优解
"""
import numpy as np

class BGA:
    def __init__(self, pop_size, dna_size, services_times):
        self.pop_size = pop_size
        self.dna_size = dna_size
        self.services_times = services_times  # 各检查室的时间
        self.project_num = len(self.services_times) - 1
        self.pop = np.zeros(shape=(self.pop_size, self.dna_size))
        self.init_pop()

    def init_pop(self):
        for i in range(self.pop_size):
            self.pop[i:] = np.random.choice([i for i in range(1, self.dna_size + 1)], size=self.dna_size, replace=False)



if __name__ == '__main__':
    bga = BGA(5, 6)
    print(bga.pop)