"""
实现短队列优先+FIFO原则的启发式算法生成解
"""
import numpy as np
from SGA import PatientRecords
from SGA import ServiceRecords


class ShortLineFirstAlgorithm:
    """调用此算法可以得到一条dna序列"""
    def __init__(self, people_num, service_time):
        self.people_num = people_num
        self.project_num = len(service_time) - 1 # 0号服务台不启用
        self.service_times = service_time
        self.people_records = PatientRecords(people_num)
        self.service_records = ServiceRecords(len(service_time), service_time)
        self.genes = [0 for _ in range(self.people_num * self.project_num)]
        self.check_table = [[1 for _ in range(self.project_num)] for _ in range(self.people_num)]

    def get_genes(self):
        """初始化之后，调用此算法可以获得一条dna"""
        self.clean_last_cache()
        return self.genes

    def clean_last_cache(self):
        """清空上一次生成的缓存"""
        self.genes = [0 for _ in range(self.people_num * self.project_num)]

    def generate_genes(self):
        """生成新的染色体"""
        pass

    def create_records(self):
        """添加记录"""
        pass

    def is_done(self):
        if np.sum(np.array(self.check_table)) == 0:
            return True
        return False



if __name__ == '__main__':
    TEST_PEOPLE_NUM = 4
    TEST_SERVER_TIMES = [
        -1,
        2,
        2,
        6
    ]

    params = {
        'people_num': TEST_PEOPLE_NUM,
        'service_time': TEST_SERVER_TIMES,
    }

    slf_algo = ShortLineFirstAlgorithm(**params)
    print(slf_algo.check_table)
