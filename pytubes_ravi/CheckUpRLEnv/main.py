import queue
from utils import log


# TODO： 事件优先级
class Event:
    """
    事件类型： MainArrive、RoomArrive、 RoomFinish
    """

    def __init__(self, obj, time, event_type):
        self.object = obj  # 保存需要操作的对象
        self.time = time  # 事件发生时间
        self.event_type = event_type  # 事件类型，str

    def __lt__(self, other):
        """
        用于实现事件优先队列
        :return: Bool
        """
        if self.time == other.get_time():
            if self.event_type == "MainArrive" and other.event_type == "RoomFinish":
                return True
            else:
                return False
        return self.time < other.get_time()

    def get_time(self):
        return self.time

    def get_object(self):
        return self.object

    def get_type(self):
        return self.event_type


class Timer:
    """
    全局时钟类
    """

    def __init__(self):
        self.time = 0

    def get_time(self):
        return self.time

    def forward(self, time):
        self.time = time

    def reset(self):
        self.time = 0


class Customer:
    def __init__(self, cid: int, timer: Timer, main_arrive, main_arrive_inter, services: list):
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


class ServiceRecord:
    """
    服务记录单，详细地记录了服务的具体细节 (对象是谁？多久开始？多久结束？)
    拥有方法finish_service用于记录完成时间
    """

    def __init__(self, customer: Customer, enter_time):
        self.customer = customer
        self.enter_time = enter_time
        self.leave_time = None

    def get_customer(self) -> Customer:
        return self.customer

    def finish_service(self, time):
        self.leave_time = time

    def get_service_time(self):
        if self.leave_time is None:
            return -1
        return self.leave_time - self.enter_time


class Service:
    """
    科室类
    """

    def __init__(self, sid: int, timer: Timer):
        self.id = sid  # 编号
        self.timer = timer  # 全局计时器
        self.busy = False  # 当前是否繁忙
        self.cur_serving = None  # 当前服务记录，传入对象应该是ServiceRecord
        self.record = []  # 服务记录表

    def isBusy(self):
        return self.busy

    def get_ave_usage(self, time):
        """
        生成该服务器的利用率
        :return: usage
        """
        square = 0
        for record in self.record:
            if time > record.leave_time:
                square += (record.leave_time - record.enter_time)
            elif record.enter_time <= time <= record.leave_time:
                square += time - record.enter_time
            else:
                pass
        return square / time if time != 0 else 0

    def dump_and_load(self, customer):
        """
        结束当前顾客的服务，载入新的顾客，若为None则设置空闲
        :param customer: 下一位顾客
        :return: 预计服务结束时间 or None
        """
        # 若服务台正忙,结束上一个顾客服务
        if self.cur_serving:
            self.cur_serving.finish_service(time=self.timer.get_time())
            log("[DEBUG] {:.5f} {:d}customer service finished.".format(self.timer.get_time(),
                                                                       self.cur_serving.customer.id))

        # 若服务台不忙
        # 当前仍旧无顾客传入
        if not customer:
            self.cur_serving = None
            self.busy = False
            return None
        else:  # 有顾客传入，开始服务
            customer.begin_service(self.id)
            # 新建一份服务表, 设置为当前服务对象，并加入服务记录中.
            new_record = ServiceRecord(customer=customer, enter_time=self.timer.get_time())
            # 保存记录
            self.record.append(new_record)
            # 设置当前记录
            self.cur_serving = new_record
            self.busy = True
            # 返回下一次允许开始服务的时间
            return self.timer.get_time() + customer.service_times[self.id]


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


def simulate():
    # s1: 向事件队列中加入所有<主队列到达事件>
    for customer in customer_list:
        event = Event(obj=customer, time=customer.main_arrive, event_type="MainArrive")
        event_queue.put(event)
        log("[DEBUG] time:{:.5f}, add ARRIVE event {:.5f}".format(timer.get_time(), customer.main_arrive))

    # s2: 事件推进
    while not event_queue.empty():
        # 取出队首事件，并推进时间至事件发生时间
        event = event_queue.get()

        timer.forward(event.get_time())
        log(event.get_type(), "于", timer.get_time(), "发生")

        state = [len(t) for t in wait_queue_list]
        yield state

        # 顾客到达主队列事件
        if event.get_type() == "MainArrive":
            # TODO: action合法校验
            customer = event.get_object()
            action = input(str(customer.id) + "号顾客选择0-2科室:")
            rindex = int(action)
            service = service_list[rindex]

            if not service.isBusy():  # 若无需排队
                next_finish_time = service.dump_and_load(customer)
                finish_event = Event(obj=service, time=next_finish_time, event_type="RoomFinish")
                event_queue.put(finish_event)
                log("[DEBUG] time{:.5f}, add FINISH event {:.5f}".format(timer.get_time(), next_finish_time))
                # 如果顾客未完成体检
                if not customer.is_done():
                    arrive_event = Event(obj=customer, time=next_finish_time, event_type="MainArrive")
                    event_queue.put(arrive_event)
                log("[DEBUG] time{:.5f}, add Again Main Arrive event {:.5f}".format(timer.get_time(), next_finish_time))
            else:  # 去排队
                customer.enter_queue(rindex)
                wait_queue_list[rindex].append(customer)
        elif event.event_type == "RoomFinish":
            service = event.get_object()
            customer = None if len(wait_queue_list[service.id]) == 0 else wait_queue_list[service.id].pop()
            next_finish_time = service.dump_and_load(customer)
            if next_finish_time:  # 若有下一个，则创建新的完成事件
                finish_event = Event(obj=service, time=next_finish_time, event_type="RoomFinish")
                event_queue.put(finish_event)
                log("[DEBUG] time{:.5f}, add FINISH event {:.5f}".format(timer.get_time(), next_finish_time))
                # 如果顾客未完成体检
                if not customer.is_done():
                    arrive_event = Event(obj=customer, time=next_finish_time, event_type="MainArrive")
                    event_queue.put(arrive_event)
                log("[DEBUG] time{:.5f}, add Main Arrive event {:.5f}".format(timer.get_time(), next_finish_time))
        else:
            log("Todo...")


if __name__ == '__main__':
    """
    设有3个科室，有4个客户
    """
    timer = Timer()
    # 初始化顾客
    customer_list = []
    c1 = Customer(0, timer, 0.0, 20.0, [20.0, 30.0, 50.0])
    c2 = Customer(1, timer, 20.0, 50.0, [12.0, 20.0, 50.0])
    c3 = Customer(2, timer, 70.0, 20.0, [10.0, 20.0, 50.0])
    c4 = Customer(3, timer, 90.0, 20.0, [10.0, 20.0, 30.0])
    customer_list.append(c1)
    customer_list.append(c2)
    customer_list.append(c3)
    customer_list.append(c4)
    # 初始化科室
    service_list = []
    s1 = Service(0, timer)
    s2 = Service(1, timer)
    s3 = Service(2, timer)
    service_list.append(s1)
    service_list.append(s2)
    service_list.append(s3)
    # 事件主队列
    event_queue = queue.PriorityQueue()
    # 等待队列
    wait_queue_list = []
    w1 = WaitQueue(timer)
    w2 = WaitQueue(timer)
    w3 = WaitQueue(timer)
    wait_queue_list.append(w1)
    wait_queue_list.append(w2)
    wait_queue_list.append(w3)

    a = simulate()
    for it in a:
        print(it)
