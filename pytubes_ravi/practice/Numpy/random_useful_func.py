import numpy as np
import matplotlib.pyplot as plt

# 设定随机种子，每次生成的随机数会相同
np.random.seed(666)

# 1 rand(d0, d1, ..., dn)返回数据在[0, 1)之间，具有均匀分布
# 期望E(x)=(a+b)/2，方差D(x)=(b-a)²/12
print('rand')
print(np.random.rand(5))
print()
print(np.random.rand(3, 4))
print()
print(np.random.rand(2, 3, 4))
print()
# 2 randn(d0, d1, ..., dn) 返回数据为标准正态分布(均值0, 方差1)
print('randn')
print(np.random.randn(5))
print()
print(np.random.randn(3, 4))
print()
print(np.random.randn(2, 3, 4))
print()
# 3 randint(low[, high, size, dtype])生成随机整数，[low, high)
# 如果high不指定，从[0, low)生成整数
print('randint')
# single return
print(np.random.randint(3))
print(np.random.randint(1, 10))
# 指定size
print(np.random.randint(1, 10, size=(2, 3, 3)))
# 4 random([size]) 生成[0.0, 1.0)的随机数
print('random')
print(np.random.random(3))
print(np.random.random(size=(2, 3)))
print(np.random.random(size=(2, 2, 3)))
# 5 choice(a[, size, replace, p]) a是一维数组，从它里面生成随机数
print('choice')
# 从range(5)中挑3个数
print(np.random.choice(5, 3))
print(np.random.choice(5, (2, 3)))
a = [2, 3, 6, 7, 9, 11]
print(np.random.choice(a, (2, 3)))
print(np.random.choice(a, (2, 3, 5)))
# shuffle 从第一维进行打散
b = np.arange(0, 11)
print('before shuffle:')
print(b)
np.random.shuffle(b)
print('after shuffle:')
print(b)
b = np.arange(20).reshape(4, 5)
print('before shuffle:')
print(b)
np.random.shuffle(b)
print('after shuffle:')
# 只会按行打散，不会按列打散（破坏实际意义）
print(b)
# 7 permutation(x) 将数组x进行随机排列
print('permutation')
# 对range(5)进行随机排列
print(np.random.permutation(5))
arr = np.arange(9).reshape(3, 3)
print(np.random.permutation(arr))
print('实际上arr并没有改变：')
print(arr)
# 8 高斯分布 按照loc平均值和scale方差值生成一个规模为size的正态分布
print('normal:')
print(np.random.normal(1, 10, 10))
print(np.random.normal(1, 10, (10, 2)))
# 9 uniform low hight 之间的均匀分布
print('uniform:')
print(np.random.uniform(1, 10, 10))
print(np.random.uniform(1, 10, (3, 4)))


# 设置-10， 10的位置取240个间隔一致的数据
x = np.linspace(-10, 10, 240)
# 随机噪声
y = np.sin(x) + np.random.rand(len(x))
plt.plot(x, y)
plt.show()
