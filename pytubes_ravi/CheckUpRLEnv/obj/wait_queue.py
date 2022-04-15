from obj.customer import Customer


class WaitRecord:
    """
    排队记录单，记录了详细的排队细节：顾客是谁？进入队伍时间？离开队伍时间？
    """

    def __init__(self, customer: Customer, enter_time):
        self.customer = customer
        self.enter_time = enter_time
        self.leave_time = None

    def leave_queue(self, time):
        self.leave_time = time

    def get_wait_time(self):
        if self.leave_time is None:
            return -1
        return self.leave_time - self.enter_time


class WaitQueue:
    """
    排队队列
    """

    def __init__(self, timer):
        self.timer = timer  # 全局计时器
        self.queue = []  # 队列FCFS
        self.record = []
        self.record_ptr = 0

    def __len__(self):
        """
        返回当前时刻的队列顾客数量
        :return: int
        """
        return len(self.queue)

    def append(self, x: Customer):
        """入队"""
        self.queue.append(x)
        self.record.append(WaitRecord(x, self.timer.get_time()))

    def pop(self) -> Customer:
        """出队"""
        self.record[self.record_ptr].leave_queue(time=self.timer.get_time())
        self.record_ptr += 1
        # 返回队首元素
        return self.queue.pop(0)


def gen_wait_queues(timer):
    return [WaitQueue(timer) for _ in range(14)]
