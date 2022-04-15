import math
import random

import numpy as np
import matplotlib.pyplot as plt

common_data = [
    [0, '采血', 60, 123, 180],
    [1, '眼科', 44, 62, 90],
    [2, '耳鼻喉科', 45, 54, 80],
    [3, '身高、血压', 30, 53, 70],
    [4, '呼气试验', 25, 35, 45],
    [5, '骨密度', 45, 59, 140],
    [6, '脑血流', 80, 129, 180],
    [7, '动脉硬化', 90, 152, 240],
]

male_data = [
    [8, '外科(男)', 25, 45, 60],
    [9, '内科(男)', 44, 66, 90],
    [10, '彩超(男)', 241, 286, 720],
]

female_data = [
    [11, '外科(女)', 75, 105, 180],
    [12, '内科(女)', 52, 85, 150],
    [13, '彩超(女)', 370, 400, 720],
]


class CheckItem:
    def __init__(self, index, name, min_service_time, mean_service_time, max_service_time):
        self.name = name
        self.ridx = index
        self.min_time = min_service_time
        self.mean_time = mean_service_time
        self.max_time = max_service_time

    def random_service_time(self):
        random_time = np.random.default_rng().triangular(self.min_time, self.mean_time, self.max_time, 1)
        return math.ceil(random_time)

    def __repr__(self):
        return f"{self.ridx}--{self.name}"

    def get_data(self):
        time = self.random_service_time()
        return [self.ridx, time]


class ItemGenerator:
    def __init__(self):
        self.common_items = [CheckItem(params[0], params[1], params[2], params[3], params[4]) for params in common_data]
        self.male_items = [CheckItem(params[0], params[1], params[2], params[3], params[4]) for params in male_data]
        self.female_items = [CheckItem(params[0], params[1], params[2], params[3], params[4]) for params in female_data]

    def generate_male_items(self):
        gen_list = [item.get_data() for item in self.male_items]
        random_num = math.ceil(np.random.default_rng().triangular(7, 9, 11))
        choose_num = random_num - len(male_data)
        items = random.sample(self.common_items, choose_num)
        gen_list.extend([item.get_data() for item in items])
        return gen_list

    def generate_female_items(self):
        gen_list = [item.get_data() for item in self.female_items]
        random_num = math.ceil(np.random.default_rng().triangular(7, 9, 11))
        choose_num = random_num - len(male_data)
        items = random.sample(self.common_items, choose_num)
        gen_list.extend([item.get_data() for item in items])
        return gen_list

    def generate_services_list(self, sex='female'):
        gen = [-1] * 14
        if sex == 'male':
            l = self.generate_male_items()
        else:
            l = self.generate_female_items()
        l.sort(key=lambda elem: elem[0])
        # 填充有效数据
        for item in l:
            gen[item[0]] = item[1]
        return gen


if __name__ == '__main__':
    ig = ItemGenerator()
    a = ig.generate_services_list()
    print(a)
