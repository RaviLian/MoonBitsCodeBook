import numpy as np

# array的三种创建方法
# 1.使用Python嵌套List
x = np.array(
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8]
    ]
)
print(x)
# array的属性
# shape：元组表示array的维度
print(x.shape)
# ndim：1个数，表示array的维度数目
print(x.ndim)
# size：1个数，array元素的个数
print(x.size)
# dtype：元素数据类型
print(x.dtype)

# 2.内置函数创建array
# 2.1 arange(start, end, step)
x = np.arange(2.0, 10.0, 1.5)
print(x)
# 2.2 ones 全1
x = np.ones((2, 2, 3), dtype=float)
print(x.shape, x)
# 2.3 ones_like 按照另一个矩阵的形状来创建
y = np.zeros((3, 4))
x = np.ones_like(y)
print(y)
# 2.4 empty未初始化的元素
x = np.empty((3, 4, 2, 5))
print(x)
# 2.5 full 设定填充值
x = np.full((3, 5), 10)
print(x)

# 3. random 模块 randn 创建array
print(np.random.randn())
print(np.random.randn(3))
print(np.random.randn(3, 2))
print(np.random.randn(3, 2, 4))

