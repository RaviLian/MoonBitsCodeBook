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