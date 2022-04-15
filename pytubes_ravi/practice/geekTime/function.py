# def 是可执行语句，这意味着函数直到被调用前，都是不存在的。
# 当程序调用函数时，def 语句才会创建一个新的函数对象，并赋予其名字。
# 主程序调用函数时，必须保证这个函数此前已经定义过，不然就会报错
# find_largest_element([8, 1, -3, 10, 0])
# NameError: name 'find_largest_element' is not defined
def find_largest_element(l):
    if not isinstance(l, list):
        print('input is not type of list')
        return
    if len(l) == 0:
        print('empty input')
        return
    largest_element = l[0]
    for item in l:
        if item > largest_element:
            largest_element = item
    print('largest element is: {}'.format(largest_element))


find_largest_element([8, 1, -3, 10, 0])


# 在函数内部调用其他函数，函数间哪个声明在前、哪个在后就无所谓
# def 是可执行语句，函数在调用之前都不存在
# 只需保证调用时，所需的函数都已经声明定义
def my_func(message):
    my_sub_func(message)  # 调用 my_sub_func() 在其声明之前不影响程序执行


def my_sub_func(message):
    print('Got a message: {}'.format(message))


my_func('hello world')


# Python 不用考虑输入的数据类型，而是将其交给具体的代码去判断执行
def my_sum(a, b):
    return a + b


# 我们把这种行为称为多态
print(my_sum(3, 5))
print(my_sum('a', 'b'))


# 其实，函数的嵌套，主要有下面两个方面的作用。
# 第一，函数的嵌套能够保证内部函数的隐私。
# 内部函数只能被外部函数所调用和访问，不会暴露在全局作用域，
# 因此，如果你的函数内部有一些隐私数据（比如数据库的用户、密码等），不想暴露在外，
# 那你就可以使用函数的的嵌套，将其封装在内部函数中，只通过外部函数来访问。比如：
# def connect_DB():
#     def get_DB_configuration():
#         ...
#         return host, username, password
#     conn = connector.connect(get_DB_configuration())
#     return conn
# 第二，合理的使用函数嵌套，能够提高程序的运行效率。我们来看下面这个例子：
# def factorial(input):
#     # validation check
#     if not isinstance(input, int):
#         raise Exception('input must be an integer.')
#     if input < 0:
#         raise Exception('input must be greater or equal to 0')
#     ...
#
#     def inner_factorial(input):
#         if input <= 1:
#             return 1
#         return input * inner_factorial(input - 1)
#
#     return inner_factorial(input)
#
#
# print(factorial(5))
# 使用递归的方式计算一个数的阶乘
# 在计算之前，需要检查输入是否合法
# 写成了函数嵌套的形式，这样一来，输入是否合法就只用检查一次
# 如果我们不使用函数嵌套，那么每调用一次递归便会检查一次，这是没有必要的，也会降低程序的运行效率

# 对于嵌套函数来说，内部函数可以访问外部函数定义的变量，但是无法修改，
# 若要修改，必须加上 nonlocal 这个关键字：
def outer():
    x = "local"

    def inner():
        nonlocal x  # nonlocal 关键字表示这里的 x 就是外部函数 outer 定义的变量 x
        x = 'nonlocal'
        print("inner:", x)

    inner()
    print("outer:", x)


outer()


# 闭包（closure）
# 闭包其实和刚刚讲的嵌套函数类似，不同的是，
# 这里外部函数返回的是一个函数，而不是一个具体的值。
# 返回的函数通常赋于一个变量，这个变量可以在后面被继续执行调用。
def nth_power(exponent):
    def exponent_of(base):
        return base ** exponent

    return exponent_of  # 返回值是 exponent_of 函数


square = nth_power(2)  # 计算一个数的平方
cube = nth_power(3)  # 计算一个数的立方
print("square:", square)
print("cube:", cube)


def nth_power_rewrite(base, exponent):
    return base ** exponent


a = nth_power_rewrite(2, 3)
b = nth_power_rewrite(4, 3)
A = cube(2)
B = cube(4)
print('a = {}, A = {}; b = {}, B = {}'.format(a, A, b, B))


# 和上面讲到的嵌套函数优点类似，函数开头需要做一些额外工作，
# 而你又需要多次调用这个函数时，将那些额外工作的代码放在外部函数，
# 就可以减少多次调用导致的不必要的开销，提高程序的运行效率

def quick_sort(array, l, r):
    def partition(array, l, r):
        x = array[r]
        i = l - 1
        for j in range(l, r):
            if array[j] <= x:
                i += 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[r] = array[r], array[i + 1]
        return i + 1

    if l < r:
        q = partition(array, l, r)
        quick_sort(array, l, q - 1)
        quick_sort(array, q + 1, r)


l1 = [5, 21, 44, 12, 19, 8, 5, 11, 10]
quick_sort(l1, 0, 8)
print(l1)