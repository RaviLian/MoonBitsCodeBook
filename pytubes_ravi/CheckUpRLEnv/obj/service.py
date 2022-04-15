from obj.customer import Customer
from utils import log
from obj.timer import Timer


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

    def __init__(self, sid: int, sname: str, timer: Timer):
        self.id = sid  # 编号
        self.name = sname
        self.timer = timer  # 全局计时器
        self.busy = False  # 当前是否繁忙
        self.cur_serving = None  # 当前服务记录，传入对象应该是ServiceRecord
        self.record = []  # 服务记录表

    def set_timer(self, t):
        self.timer = t

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

    def __repr__(self):
        return f"{self.id}--{self.name}"

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


def services_init(timer):
    service_data = ['采血', '眼科', '耳鼻喉科', '身高、血压', '呼气试验', '骨密度', '脑血流', '动脉硬化', '外科(男)', '内科(男)', '彩超(男)', '外科(女)',
                    '内科(女)', '彩超(女)']
    service_list = [Service(i, service_data[i], timer) for i in range(len(service_data))]
    return service_list


if __name__ == '__main__':
    print(services_init())
