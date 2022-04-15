# 匿名函数的格式
# lambda argument1, argument2,... argumentN : expression
from functools import reduce

square = lambda x: x ** x
a = square(3)
print(a)
# 匿名函数 lambda 和常规函数一样，返回的都是一个函数对象（function object）
# 第一，lambda 是一个表达式（expression），并不是一个语句（statement）。
# lambda 可以用在一些常规函数 def 不能用的地方，
# 比如，lambda 可以用在列表内部，而常规函数却不能
print([(lambda x: x * x)(x) for x in range(10)])
# lambda 可以被用作某些函数的参数，而常规函数 def 也不能
l = [(1, 20), (3, 0), (9, 10), (2, -1)]
l.sort(key=lambda x: x[1])  # 按列表中元祖的第二个元素排序
print(l)
# 第二，lambda 的主体是只有一行的简单表达式，并不能扩展成一个多行的代码块。
# lambda 专注于简单的任务，而常规函数则负责更复杂的多行逻辑
# 只进行一次简单操作的逻辑使用lambda
# map函数，接受一个函数和一个Iterable。
# 将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
squared = map(lambda x: x ** 2, [1, 2, 3, 4, 5])
for elem in squared:
    print(elem, end=' ')
print()


# 所谓函数式编程，是指代码中每一块都是不可变的（immutable），
# 都由纯函数（pure function）的形式组成。
# 这里的纯函数，是指函数本身相互独立、互不影响，
# 对于相同的输入，总会有相同的输出，没有任何副作用。
# 例： 使元素成为原2倍
def multiply_2(l):
    for index in range(0, len(l)):
        l[index] *= 2
    return l


# 这段代码就不是一个纯函数的形式，因为列表中元素的值被改变了，
# 如果我多次调用 multiply_2() 这个函数，那么每次得到的结果都不一样。
# 要想让它成为一个纯函数的形式，就得写成下面这种形式，重新创建一个新的列表并返回。
def multiply_2_pure(l):
    new_list = []
    for item in l:
        new_list.append(item * 2)
    return new_list


# 函数式编程的优点，主要在于其纯函数和不可变的特性使程序更加健壮，
# 易于调试（debug）和测试；缺点主要在于限制多，难写。


# filter(function, iterable) 函数
# filter() 函数表示对 iterable 中的每个元素，
# 都使用 function 判断，并返回 True 或者 False，
# 最后将返回 True 的元素组成一个新的可遍历的集合
l = [1, 2, 3, 4, 5]
new_list = filter(lambda x: x % 2 == 0, l)  # [2, 4]
print('[1, 2, 3, 4, 5] 偶数 filter:')
for elem in new_list:
    print(elem, end=' ')
print()

# reduce(function, iterable) 函数，它通常用来对一个集合做一些累积操作
# function 同样是一个函数对象，规定它有两个参数，
# 表示对 iterable 中的每个元素以及上一次调用后的结果，运用 function 进行计算，
# 所以最后返回的是一个单独的数值。
l = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, l)  # 1*2*3*4*5 = 120
print('reduce:', product)

# 对字典的值进行排序
d = {'mike': 10, 'lucy': 2, 'ben': 30}
ds = sorted(d.items(), key=lambda x: x[1], reverse=True)
print('ds.Type:{}, ds:{}'.format(type(ds), dict(ds)))
