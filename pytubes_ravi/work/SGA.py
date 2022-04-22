"""
单种群遗传算法
染色体chromosome:
"""
from collections import deque

class PatientRecords:
    def __init__(self, total_num):
        self.total = total_num
        self.store = self.__init_store()

    def __init_store(self):
        store = [deque() for _ in range(self.total)]
        return store

    def add_record(self, pidx, record):
        self.store[pidx].append(record)


if __name__ == '__main__':
    prs = PatientRecords(20)
    prs.add_record(3, [0, 1, 2])

