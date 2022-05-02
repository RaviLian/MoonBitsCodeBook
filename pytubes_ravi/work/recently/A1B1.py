"""
第一轮分配，尽量均匀时间分配
启发式解，每一轮分配，顾客按照剩余服务时间排队，剩余服务时间最长的优先分配;
每一轮分配，优先分配服务时长最长的
"""
from operator import attrgetter

cost_time_lookup = [
    3,  # 0体质测试   4
    3,  # 1内科      4
    4,  # 2外科      3
    2,  # 3眼耳口鼻科 5
    3,  # 4验血      4
    2,  # 5心电图    5
    5,  # 6X光      3
    6,  # 7B超      2
]  # 共28分钟

# cost_time_lookup = [
#     3, 3, 4, 6
# ]

total_people = 30
project_num = len(cost_time_lookup)
common_actions = [(i, cost_time_lookup[i]) for i in range(project_num)]
T_W = 15  # 等待阈值
GAMMA = 5  # 惩罚系数


class Patient:
    def __init__(self, pid):
        self.pid = pid
        self.actions = [(i, cost_time_lookup[i]) for i in range(project_num)]

    def remove_actions(self, action):
        self.actions.remove(action)

    @property
    def rest_time(self):
        return sum([a[1] for a in self.actions])

    def __repr__(self):
        return "p-" + str(self.pid)

class HeuristicSolution:
    """启发式解"""

    def __init__(self):
        self.patient_table = [[] for _ in range(total_people)]
        self.project_table = [[] for _ in range(project_num)]
        self.sequence = []  # 最终生成的序列
        self.operations = []  # 保存分配动作[pidx, sidx, cost_time]
        self.patients = [Patient(i) for i in range(total_people)]

    def build_table(self):
        """建表"""
        self.first_build_30()
        # 根据剩余服务时间排序
        this_seq = sorted([pat for pat in self.patients], key=attrgetter('rest_time'), reverse=True)
        for patient in this_seq:
            pass

    def first_build_30(self):
        for i in range(4):
            self.patients[i].remove_actions(common_actions[0])
            self.create_records(i, common_actions[0])
        for i in range(4, 8):
            self.patients[i].remove_actions(common_actions[1])
            self.create_records(i, common_actions[1])
        for i in range(8, 11):
            self.patients[i].remove_actions(common_actions[2])
            self.create_records(i, common_actions[2])
        for i in range(11, 16):
            self.patients[i].remove_actions(common_actions[3])
            self.create_records(i, common_actions[3])
        for i in range(16, 20):
            self.patients[i].remove_actions(common_actions[4])
            self.create_records(i, common_actions[4])
        for i in range(20, 25):
            self.patients[i].remove_actions(common_actions[5])
            self.create_records(i, common_actions[5])
        for i in range(25, 28):
            self.patients[i].remove_actions(common_actions[6])
            self.create_records(i, common_actions[6])
        for i in range(28, 30):
            self.patients[i].remove_actions(common_actions[7])
            self.create_records(i, common_actions[7])

    def create_records(self, pid, action):
        sid, cost_time = action[0], action[1]
        patient_last_end_time = self.get_patient_last_end(pid)
        project_last_end_time = self.get_project_last_end(sid)
        start_time = max(patient_last_end_time, project_last_end_time)
        end_time = start_time + cost_time
        self.patient_table[pid].append([sid, start_time, end_time])
        self.project_table[sid].append([pid, start_time, end_time])

    def get_patient_last_end(self, pid):
        if len(self.patient_table[pid]) == 0:
            return 0
        else:
            self.patient_table[pid].sort(key=lambda e: e[2])
            return self.patient_table[pid][-1][2]

    def get_project_last_end(self, sid):
        if len(self.project_table[sid]) == 0:
            return 0
        else:
            self.project_table[sid].sort(key=lambda e: e[2])
            return self.project_table[sid][-1][2]

    def compute_fitness(self):
        global GAMMA
        global T_W
        people_records, project_records = self.translate()
        W_sum = 0
        w_thanT_sum = 0
        tmp_lates = []
        for records in people_records:
            records.sort(key=lambda e: e[2])
            tmp_lates.append(records[-1][2])
            for i in range(len(records)):
                if i == 0:
                    wait_time = records[i][1] - 0
                    if wait_time == 0:
                        continue
                    W_sum += wait_time
                    if wait_time - T_W > 0:
                        w_thanT_sum += (wait_time - T_W)
                else:
                    wait_time = records[i][1] - records[i - 1][2]
                    W_sum += wait_time
                    if wait_time - T_W > 0:
                        w_thanT_sum += (wait_time - T_W)
        maxF = max(tmp_lates)
        fitness = maxF + W_sum + GAMMA * w_thanT_sum
        return fitness, maxF, W_sum, w_thanT_sum

    def print_patient_table(self):
        print("patient_table:")
        for p in self.patient_table:
            print(p)

    def print_project_table(self):
        print("project_table:")
        for p in self.project_table:
            print(p)


if __name__ == '__main__':
    heur = HeuristicSolution()
    heur.build_table()
    heur.print_patient_table()
    heur.print_project_table()
