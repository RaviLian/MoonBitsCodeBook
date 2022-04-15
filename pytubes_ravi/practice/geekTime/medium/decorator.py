import functools
import time

"""
所谓的装饰器，其实就是通过装饰器函数，来修改原函数的一些功能，使得原函数不需要修改
"""


def my_decorator(func):
    def wrapper():
        print('wrapper of decorator')
        func()

    return wrapper


def greet():
    print('hello world')


# 变量 greet 指向了内部函数 wrapper()，
# 而内部函数 wrapper() 中又会调用原函数 greet()，
# 因此，最后调用 greet() 时，就会先打印'wrapper of decorator'，然后输出'hello world'。
#
# 这里的函数 my_decorator() 就是一个装饰器，
# 它把真正需要执行的函数 greet() 包裹在其中，并且改变了它的行为，
# 但是原函数 greet() 不变。
greet = my_decorator(greet)
greet()


def welcome(func):
    def wrapper(title):
        print('Welcome to our meeting!')
        func(title)

    return wrapper


@welcome
def topic(title):
    print('Our topic is ', title.upper())


topic('ieee')


# 多个参数
def repeat(num):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num):
                print('wrapper of decorator')
                func(*args, **kwargs)

        return wrapper

    return my_decorator


@repeat(4)
def greet(message):
    print(message)


greet('hello world')


# 类装饰器主要依赖于函数__call_()，每当你调用一个类的示例时，函数__call__()就会被执行一次
class Count:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print('num of calls is: {}'.format(self.num_calls))
        return self.func(*args, **kwargs)


@Count
def example():
    print("hello python")


# 1
example()
# 2
example()


def my_decorator1(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('execute decorator1')
        func(*args, **kwargs)

    return wrapper


def my_decorator2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('execute decorator2')
        func(*args, **kwargs)

    return wrapper


@my_decorator1
@my_decorator2
def greet(message):
    print(message)


# decorator1(decorator2(decorator3(func)))
# 执行顺序由里到外
greet('hello decorator -r')


# 应用举例
def log_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print('{} took {} ms'.format(func.__name__, (end - start) * 1000))
        return res

    return wrapper


@log_execution_time
def gen_li1(num):
    li = []
    for i in range(num):
        li.append(i)
    return li


@log_execution_time
def gen_li2(num):
    li = [i for i in range(num)]
    return li


n1 = 10000
# 比较得出列表生成式浪费的时间更多
gen_li1(n1)
gen_li2(n1)
# gen_li1 took 0.681141042150557 ms
# gen_li2 took 0.2495420048944652 ms
