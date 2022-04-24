"""
单种群遗传算法
染色体chromosome:
"""
import numpy as np


class PatientRecords:
    """客户必须+1，因为0不是合法下标"""
    def __init__(self, total_num):
        self.total = total_num
        self.store = self.__init_store()

    def __init_store(self):
        # 舍弃0位置,不保存
        store = [[] for _ in range(self.total + 1)]
        return store

    def add_record(self, pidx, record):
        self.check_self(pidx, record)
        self.store[pidx].append(record)

    def check_self(self, pidx, record):
        st = record[1]
        records = self.store[pidx]
        for record in records:
            if record[1] == st:
                print("p-insert-record:", record)
                print("p-records:", records)
                raise ValueError("同一时间在两个科室接受服务")

    def get_last_project_end(self, pidx):
        """得到上一项目的结束时间"""
        records = self.store[pidx]
        if len(records) == 0:
            return 0
        records.sort(key=lambda e: e[2])
        return records[-1][2]


class ServiceRecords:
    """服务台数目+1，因为0号不是合法服务台"""
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
        store = [[] for _ in range(self.total)]
        return store

    def add_record(self, service_idx, record):
        """
        :param service_idx: 服务台编号
        :param record: [客户index, 开始检查时间, 结束检查时间]
        """
        self.check_self(service_idx, record)
        self.store[service_idx].append(record)

    def check_self(self, service_idx, record):
        st = record[1]
        records = self.store[service_idx]
        for record in records:
            if st == record[1]:
                print("s-insert-record:", record)
                print("s-records:", records)
                raise ValueError("同一时刻服务一个客户")

    def get_idle_times(self, service_idx):
        """得到该服务台的空闲时间区间"""
        service = self.store[service_idx]
        idles = []
        if len(service) == 0:
            idles.append([0, 240])
            return idles
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

        return idles


class DNA:
    def __init__(self, people_num, service_times):
        self.bound = people_num * (len(service_times) - 1)
        self.patient_records = PatientRecords(people_num)
        self.service_records = ServiceRecords(len(service_times), service_times)
        self.fitness = 0  # 适应度值
        self.genes = self.__init_dna()

    def __init_dna(self):
        return np.random.choice([i for i in range(1, self.bound + 1)], size=self.bound, replace=False)

    def __getitem__(self, item):
        """返回dna保存的值"""
        return self.genes[item]

    def __repr__(self):
        return self.genes.__str__()




def compute_fitness(dna):
    """
    计算一条DNA解的适应度值
    顾客总等待时间 + max(科室结束服务时间) + 超阈值等待时间
    """
    patient_status = dna.patient_records.store
    service_status = dna.service_records.store
    max_F = get_max_makespan(service_status)
    T_W = 15
    gamma = 10
    W_sum = 0
    w_thanT_sum = 0
    for records in patient_status:
        for i in range(1, len(records)):
            wait_time = records[i][1] - records[i-1][2]
            W_sum += wait_time
            if wait_time - T_W > 0:
                w_thanT_sum += wait_time - T_W
    fitn = max_F + W_sum + w_thanT_sum * gamma
    return fitn



def get_max_makespan(service_status):
    F = []
    for i in range(1, len(service_status)):
        recs = service_status[i]
        recs.sort(key=lambda a: a[2])
        F.append(recs[-1][2])
    return max(F)

class SGA:
    def __init__(self, people_num, service_times, cross_rate, mutation_rate, pop_size):
        self.people_num = people_num
        self.service_times = service_times
        self.project_num = len(service_times) - 1
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
        """解码,之后可以获得种群的fitness之和"""
        for dna in self.pop:
            self.translate_dna(dna)
        print(self.get_fitness())

    def translate_dna(self, dna):
        """单条dna解码，保存状态并计算适应度"""
        # 创建记录
        for gene in dna:
            self.create_records(gene, dna)
        # 计算指标
        dna.fitness = compute_fitness(dna)

    def check_record(self, records, record):
        """检查相同记录"""
        for rec in records:
            if rec[1] == record[1]:
                return True

    def filter_checked(self, records, times):
        """过滤可能造成相同记录的时间段"""
        if len(times) == 0:
            return []
        filtered_times = [ti for ti in times if self.check_record(records, ti) is False]
        return filtered_times

    def create_records(self, gene, dna):
        """解码后为客户和服务台分别创建一条记录"""
        pidx, sidx = self.get2index(gene)
        consume_time = self.service_times[sidx]

        # 插入记录
        p_status = dna.patient_records  # 当前dna的客户表格
        ser_status = dna.service_records  # 当前dna的服务台表格

        last_end_time = p_status.get_last_project_end(pidx) # 上一项目结束时间
        idles = ser_status.get_idle_times(sidx)  # 当前服务台sidx的空闲区间
        if len(idles) == 1 and idles[0][0] == 0 and idles[0][1] == 240:  # 科室没有人被分配
            cur_start_time = max(last_end_time, 0)
            cur_end_time = cur_start_time + consume_time # 得到结束时间
            p_status.add_record(pidx, [sidx, cur_start_time, cur_end_time])
            try:
                ser_status.add_record(sidx, [pidx, cur_start_time, cur_end_time])
            except ValueError:
                print("第一条数据有错!")

        else:
            # 空闲时间符合插入记录的

            enough = [time for time in idles if time[1] - time[0] > consume_time]
            enough = self.filter_checked(ser_status.store[sidx], enough)
            # 根据起始时间排序
            enough.sort(key=lambda e: e[0])
            if len(enough) > 0:  # 有足够时间
                idle = enough[0]
                cur_start_time = max(last_end_time, idle[0])
                cur_end_time = cur_start_time + consume_time
                p_status.add_record(pidx, [sidx, cur_start_time, cur_end_time])
                ser_status.add_record(sidx, [pidx, cur_start_time, cur_end_time])



            else:  # 没有足够时间, 设置有超时的
                records = ser_status.store[sidx]
                records.sort(key=lambda a:a[2])
                cur_start_time = max(last_end_time, records[-1][2])
                cur_end_time = cur_start_time + consume_time
                p_status.add_record(pidx, [sidx, cur_start_time, cur_end_time])
                ser_status.add_record(sidx, [pidx, cur_start_time, cur_end_time])

    def get_fitness(self):
        """获取整个种群的fitness"""
        all_fit = 0
        for dna in self.pop:
            all_fit += dna.fitness
        return all_fit

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
        -1, # 0无
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
    sga.translate()



