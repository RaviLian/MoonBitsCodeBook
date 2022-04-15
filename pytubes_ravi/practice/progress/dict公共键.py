from random import randint, sample
from functools import reduce

player = ['LeBron James', 
        'Kevin Durant', 
        'Anthony Davis', 
        'James Harden',
        'Stephen Curry',
        'Russell Westbrook',
        ]
# 生成进球球员Name
# sample(player, randint(3, 6))
# name 为key，表示进球球员， 随机生成其进球数目
round1 = {name: randint(1, 4) for name in sample(player, randint(3, 6))}
round2 = {name: randint(1, 4) for name in sample(player, randint(3, 6))}
round3 = {name: randint(1, 4) for name in sample(player, randint(3, 6))}
print('round1: ', round1)
print('round2: ', round2)
print('round3: ', round3)

# 得到每个字典的key
map1 = map(dict.keys, [round1, round2, round3])
# 将每个字典的key转换为集合set
map2 = map(set, map1)
# 使用functiontools中的reduce函数利用set的基本运算&求出公共元素
common_keys = reduce(lambda a, b : a & b, map2)
print(common_keys)