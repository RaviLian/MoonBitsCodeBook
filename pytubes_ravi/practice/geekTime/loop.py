# for item in <iterable>:
#     ...
d = {'name': 'james', 'age': 22, 'gender': 'male'}
# 字典中只有key是iterable
for k in d:
    print(k, end=' ')
print()

for v in d.values():
    print(v, end=' ')
print()

for k, v in d.items():
    print('[key:{}, value:{}]'.format(k, v))

# 内置的函数 enumerate()用它来遍历集合，不仅返回每个元素，并且还返回其对应的索引
l = [1, 2, 8, 2, 4, 5, 9]
for index, item in enumerate(l):
    print('[{}]:{}'.format(index, item), end=' ')
print()

# expression1 if condition else expression2 for item in iterable
# 等价于
# for item in iterable:
#     if condition:
#         expression1
#     else:
#         expression2

# y = 2*|x| + 5
# mine : y = [2 * x + 5 if x > 0 else 2 * (-x) + 5 for x in range(-3, 4)]
x = [-3, -2, -1, 0, 1, 2, 3]
y = [value * 2 + 5 if value > 0 else -value * 2 + 5 for value in x]
print(y)

# 过滤掉长度小于等于 3 的单词
# 批量处理文本，先按,进行拆分，然后对每个单词进行strip()去除首尾空格,
# 若无else
# expression for item in iterable if condition
text = ' Today,  is, Sunday '
text_list = [s.strip() for s in text.split(',') if len(s.strip()) > 3]
print(text_list)

attributes = ['name', 'dob', 'gender']
values = [['jason', '2000-01-01', 'male'],
['mike', '1999-01-01', 'male'],
['nancy', '2001-02-01', 'female']
]

li = []
for line in values:
    d = {}
    for i in range(3):
        d[attributes[i]] = line[i]
    li.append(d)

l2 = [dict(zip(attributes, value)) for value in values]
print(l2)
