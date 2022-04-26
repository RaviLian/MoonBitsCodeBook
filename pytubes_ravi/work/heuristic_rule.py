"""
实现短队列优先+FIFO原则的启发式算法生成解
"""
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

