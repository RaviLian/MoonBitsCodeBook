import datetime
import time


class XboxOne:
    def __init__(self):
        self.name = "XboxOne"

    def play(self):
        return "使用%s打游戏" % self.name


class PS4:
    def __init__(self):
        self.name = "PlayStation4"

    def play(self):
        return "使用%s打游戏" % self.name


if __name__ == '__main__':
    gamer = XboxOne
    print("在{}时刻{}".format(datetime.datetime.now(), gamer().play()))
    time.sleep(1)
    gamer = PS4
    print("在{}时刻{}".format(datetime.datetime.now(), gamer().play()))
