"""
1. 随机产生初始解，建立初始种群，种群规模为Z；进行解码和适应度计算
2. 使用交叉算子和突变算子对当前种群中对解进行重组，产生后代，形成新的种群。进行解码和适应度计算
3. 迭代：重复1-2，直到解一定代数内最优值没有发生明显改进，输出当前最优解
"""
import numpy as np

cost_time_lookup = [
        3,  # 0体质测试
        3,  # 1内科
        4,  # 2外科
        2,  # 3眼耳口鼻科
        3,  # 4验血
        2,  # 5心电图
        5,  # 6X光
        6,  # 7B超
]  # 共28分钟

total_people = 10
project_num = len(cost_time_lookup)

def translate_operation(opt):
    """解码操作"""
    opt = opt - 1
    return opt // project_num, opt % project_num


class Chromosome:
    def __init__(self, sequence):
        self.sequence = sequence  # list DNA序列
        self.fitness = None
        self.makespan = None
        self.maxF = None
        self.total_wait = None
        self.greater_than_threshold = None

    def translate(self):
        global cost_time_lookup
        global total_people
        global project_num
        people_records = [[] for _ in range(total_people)]
        project_records = [[] for _ in range(project_num)]
        for operation in self.sequence:
            people_index, project_index = translate_operation(operation)
            cost_time = cost_time_lookup[project_index]

            people = people_records[people_index] # 客户的所有记录
            project = project_records[project_index] # 项目的所有记录
            # 创建记录
            people_last_end_time = self.get_people_last_end(people) # 人有空的最早时间
            project_last_ends = self.get_project_last_end(project)

            # 科室第一条记录
            if type(project_last_ends) == int:
                start_time = people_last_end_time
                end_time = start_time + cost_time
                people.append([project_index, start_time, end_time])
                project.append([people_index, start_time, end_time])

            if type(project_last_ends) == list:

                tmp_start = self.get_middle_start_time(project_last_ends, cost_time, people_last_end_time)
                if tmp_start == -1:
                    # 科室末尾插入
                    start_time = max(people_last_end_time, project_last_ends[-1])
                    end_time = start_time + cost_time
                    people.append([project_index, start_time, end_time])
                    project.append([people_index, start_time, end_time])
                else:
                    # 科室中间插入
                    start_time = tmp_start
                    end_time = start_time + cost_time
                    people.append([project_index, start_time, end_time])
                    project.append([people_index, start_time, end_time])
        return people_records, project_records



    @staticmethod
    def get_people_last_end(people_table):
        if len(people_table) == 0:
            return 0
        else:
            people_table.sort(key=lambda e: e[2])
            return people_table[-1][2]

    @staticmethod
    def get_project_last_end(project_table):
        """得到项目表中每个人的结束时间"""
        if len(project_table) == 0:
            return 0
        else:
            project_table.sort(key=lambda e: e[2])
            return [record[-1] for record in project_table]

    @staticmethod
    def get_middle_start_time(end_time_list, cost_time, people_start):
        """
        如果二者间时间间隔大于2倍的检查时间，表明有足够的时间
        如果后者 - 客户开始时间仍大于2倍的检查时间(要减去之前分配的一次检查)，则表明可以插入
        否则，只能在末尾插入
        """
        for i in range(1, len(end_time_list)):
            if end_time_list[i] - end_time_list[i - 1] >= 2 * cost_time:
                if end_time_list[i] - people_start >= 2 * cost_time:
                    return max(people_start, end_time_list[i - 1])
        return -1





if __name__ == '__main__':
    seq = [27, 59, 20, 21, 22, 49, 66, 40, 38, 8, 65, 36, 15, 14, 46, 28, 52, 56, 17, 53, 35, 41, 75, 80, 34, 47, 71, 23, 11, 61, 42, 77, 37, 70, 3, 24, 13, 26, 30, 29, 74, 6, 10, 18, 2, 19, 50, 39, 9, 43, 48, 76, 33, 51, 72, 62, 58, 12, 73, 4, 67, 7, 5, 32, 16, 31, 45, 79, 60, 64, 54, 68, 1, 63, 57, 69, 78, 25, 55, 44]
    c = Chromosome(seq)
    pi, se = c.translate()
    for p in pi:
        print(p)
    print("----")
    for s in se:
        print(s)


