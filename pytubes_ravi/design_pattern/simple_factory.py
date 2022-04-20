from abc import ABCMeta, abstractmethod


# 抽象产品角色，以什么样的表现去使用
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass


# 产品角色
class Alipay(Payment):
    def __init__(self, use_huabei=False):
        self.use_huabei = use_huabei

    def pay(self, money):
        if self.use_huabei:
            print("花呗支付了{0}元!".format(money))
        else:
            print("支付宝余额支付了{0}元!".format(money))


# 产品角色
class WechatPay(Payment):
    def pay(self, money):
        print("微信支付了%d元!" % (money))


# 工厂类角色
class PaymentFactory:
    @staticmethod
    def create_payment(method):
        if method == 'Alipay':
            return Alipay()
        elif method == 'WechatPay':
            return WechatPay()
        elif method == 'HuabeiPay':
            return Alipay(use_huabei=True)
        else:
            raise TypeError('No such payment named %s' % method)


if __name__ == '__main__':
    p = PaymentFactory.create_payment('HuabeiPay')
    p.pay(12)
