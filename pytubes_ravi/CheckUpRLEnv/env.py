import numpy as np
from obj.timer import *
from gym import spaces
from obj.customer import *
from obj.check_item import *
from obj.service import *
from obj.wait_queue import *
from obj.event import *
import queue


class CheckUpEnv:
    def __init__(self, is_train, forward):
        self.timer = Timer()
        self.is_train = is_train
        self.forward = forward
        self.observation_space = spaces.Box(low=-9999, high=9999, shape=(self.forward,), dtype=np.float)
        self.action_space = spaces.Box(low=-9999, high=9999, shape=(1,), dtype=np.float)

        # 客户列表, 客户管理器,并设置全局计时器
        self.customer_list = gen_customer(self.timer, 170)
        # 科室列表，科室管理器，并设置全局计时器
        self.services_list = services_init(self.timer)
        # 排队队列管理器，并设置全局计时器
        self.wait_queues = gen_wait_queues(self.timer)

        # 事件队列
        self.even_queue = queue.PriorityQueue()
        # 填充到达事件
        for customer in self.customer_list:
            event = Event(obj=customer, time=customer.main_arrive, event_type="MainArrive")
            self.even_queue.put(event)

    def reset(self):
        """初始化环境"""
        self.timer.reset()
        self.customer_list = gen_customer(self.timer, 170)
        self.services_list = services_init(self.timer)
        self.wait_queues = gen_wait_queues(self.timer)

    def get_current_state(self):
        wq_state = [len(wq) for wq in self.wait_queues]
        sev_state = [1 if sev.isBusy() else 0 for sev in self.services_list]
        wq_state = np.array(wq_state)
        sev_state = np.array(sev_state)
        state = wq_state + sev_state
        return state

    def step(self, action):
        pass

    def close(self):
        return None

    def seed(self, seed):
        return

    def render(self):
        return None


if __name__ == '__main__':
    c = CheckUpEnv(is_train=True, forward=8)
    print(c.get_current_state())
