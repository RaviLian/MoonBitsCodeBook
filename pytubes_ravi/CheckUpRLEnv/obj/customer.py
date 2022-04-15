import random

from obj.check_item import ItemGenerator
import matplotlib.pyplot as plt
from obj.timer import Timer
import numpy as np


class Customer:
    def __init__(self, cid: int, timer, main_arrive, main_arrive_inter, services: list):
        """
        顾客类
        :param cid:  顾客编号
        :param timer: 全局计时器
        :param main_arrive: 主队列到达时间轴时刻
        :param main_arrive_inter: 主队列下一位顾客到达的间隔时间
        :param services: list，存放实际各科室检查消耗时间，-1为无需前往的科室
        """
        self.id = cid
        self.timer = timer
        self.main_arrive = main_arrive
        self.main_arrive_inter = main_arrive_inter
        self.service_times = services
        self.total_rooms = len(services)

        # 是否需要前往某科室，动态变化
        self.need_check = [1 if s != -1 else 0 for s in services]
        # 是否第一次进入主队列
        self.is_first = True
        # 各队列开始等待时间记录
        self.begin_wait_times = [0 for _ in range(len(services))]
        # 各队列开始服务时间记录
        self.begin_service_times = [0 for _ in range(len(services))]

    def set_timer(self, t):
        self.timer = t

    def enter_queue(self, rindex):
        self.begin_wait_times[rindex] = self.timer.get_time()

    def begin_service(self, rindex):
        self.begin_service_times[rindex] = self.timer.get_time()
        self.need_check[rindex] = 0

    def get_wait_length(self, rindex):
        """得到某科室的等待时间"""
        return self.begin_service_times[rindex] - self.begin_wait_times[rindex] if self.begin_wait_times[rindex] else 0

    def get_cur_mean_wait(self):
        """
        获得当前平均等待时间
        :return:
        """
        res = [self.get_wait_length(r) for r in range(self.total_rooms)]
        count = 0
        sums = 0
        for item in res:
            if item != 0:
                count += 1
                sums += item
        return sums / count

    def get_cur_max_wait(self):
        """
        获得当前最大等待时间
        :return:
        """
        res = [self.get_wait_length(r) for r in range(self.total_rooms)]
        return max(res)

    def is_done(self):
        for i in self.need_check:
            if i == 1:
                return False
        return True

    def __repr__(self):
        return f"{self.id}--到达时间:{self.main_arrive}--检查时间:{self.service_times}"


def get_arrive_inter_list(total_nums=170):
    """生成170个人的到达间隔时间"""
    s1_nums = total_nums // 7 * 4
    s2_nums = total_nums // 7 * 2
    s3_nums = total_nums - s1_nums - s2_nums
    s1 = np.random.default_rng().poisson(30, s1_nums)
    s2 = np.random.default_rng().poisson(45, s2_nums)
    s3 = np.random.default_rng().poisson(96, s3_nums)
    arrive_inters = []
    arrive_inters.extend(s1)
    arrive_inters.extend(s2)
    arrive_inters.extend(s3)
    return arrive_inters


def gen_customer(timer, total_nums=170):
    """传入队列前需要为客户赋值全局Timer"""
    # 到达间隔表
    arrive_inters = get_arrive_inter_list(total_nums)
    ig = ItemGenerator()
    male_nums = total_nums // 2
    female_nums = total_nums - male_nums

    # 项目表
    services_lists = []
    for i in range(male_nums):
        services_lists.append(ig.generate_services_list(sex='male'))
    for i in range(female_nums):
        services_lists.append(ig.generate_services_list())
    # 打乱顺序
    random.shuffle(services_lists)
    # 客户表
    cus_list = []
    cur_time = 0
    for i in range(total_nums):
        cus_list.append(Customer(i, timer, cur_time, arrive_inters[i], services_lists[i]))
        cur_time += arrive_inters[i]
    return cus_list


if __name__ == '__main__':
    a = gen_customer(170)
    for i in a:
        print(i)
