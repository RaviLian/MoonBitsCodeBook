# 索引切片被修改，其本体也会被修改
import numpy as np

x = np.arange(10)
X = np.arange(20).reshape(4, 5)
print(x)
# 1.基础索引---精确索引
# 1.1 一维数组
print(x[2], x[-1])
print(x[2:4])
print(x[2:-1])
print(x[-3:])
print(x[:-3])
# 1.2 二维数组
print(X)
# 先取最后一行，再取第三列
print(X[-1, 2])
# 筛选第三行所有列
print(X[2])
# 筛选除最后一行多所有行
print(X[:-1])
# 筛选多行多列 前两行的三列四列
print(X[:2, 2:4])
# 筛选所有行多某一列
print(X[:, 2])
# 1.3 多维数组
Y = np.random.randn(2, 3, 5)
print(Y)
print("取Y的第二面的前三列")
print(Y[1, :, :3])

# 2.神奇索引
print('神奇索引')
# 2.1 1维数组
# 生成10个随机数
arr = np.random.randint(1, 100, 10)
print(arr)
# 取最大值对应的三个下标，使用下标找到元素
print(arr.argsort()[-3:])
print(arr[arr.argsort()[-3:]])
# 2.2 2维数组
X = np.arange(20).reshape(4, 5)
print(X)
# 筛选多行，列可以省略
print(X[[0, 2]])  # 相当于 X[[0, 2], :]
# 筛选多列，行不能省略
print(X[:, [0, 3, 2]])
# 同时制定行列列表，返回(0,1),(2,3),(3,4)的数字
print('-------------------返回数字')
print(X[[0, 2, 3], [1, 3, 4]])

# 3 布尔索引
# 3.1 一维数组
x = np.arange(12)
print('x > 5:')
print(x > 5)
print('返回大于5的数集合x[x>5]:')
print(x[x > 5])

# 3.2 二维数组
print(X)
# 降维度
print('X[X>6]:')
print(X[X > 6])
# 第三列大于5的全部行筛选出来
print(X[:, 3] > 5)
print(X[X[:, 3] > 5])
