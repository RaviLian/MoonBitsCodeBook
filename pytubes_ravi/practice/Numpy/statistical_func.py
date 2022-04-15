import numpy as np

arr = np.arange(12).reshape(3, 4)
print('arr:')
print(arr)

"""
axis用于指定计算轴为行或者列，如果不指定，那么会计算所有元素
"""
# 1. 加和
print('np.sum(arr):', np.sum(arr))
# 2.乘法
print("np.prod(arr):", np.prod(arr))
# 3
print("np.cumsum(arr):", np.cumsum(arr))
# 4
print("np.cumprod(arr):", np.cumprod(arr))
# 5
print("max and min:", np.max(arr), np.min(arr))
# 6
print("将数据从小到大进行排列，按照百分比位置取数", np.percentile(arr, [25, 50, 75]))
print("将数据从小到大进行排列，按照百分比位置取数", np.quantile(arr, [0.25, 0.5, 0.75]))
# 7 中位数
print("中位数是:", np.median(arr))
# 8
print("平均值:", np.mean(arr))
# 9
print("标准差（方差的平方根）:", np.std(arr))
# 10
print("方差:", np.var(arr))
# 11 加权平均
print("生成权重:")
weights = np.random.rand(*arr.shape)
print(weights)
print("加权平均:", np.average(arr, weights=weights))

"""
axis = 0代表行
axis = 1代表列
理解：
axis = 0代表把行消解掉（仅剩一行）；代表跨行计算
axis = 1代表把列消解掉（仅剩一列）；代表跨列计算
"""
print("arr:")
print(arr)
print("np.sum(arr, axis=0) = ", np.sum(arr, axis=0))
print("np.sum(arr, axis=1) = ", np.sum(arr, axis=1))
print("np.cumsum(arr, axis=0) =  ", np.cumsum(arr, axis=0))
print("np.cumsum(arr, axis=1) =  ", np.cumsum(arr, axis=1))

# 例子:
"""
arr:
[[ 0  1  2  3](样本1)
 [ 4  5  6  7](样本2)
 [ 8  9 10 11]](样本3)
  f1  f2 f3 f4
 每一行对应一个样本的数据
 每一列代表样本的一个特征
"""
# 求出每一列的均值
mean = np.mean(arr, axis=0)
print("均值:", mean)
# 计算每一列的标准差
std = np.std(arr, axis=0)
print("标准差:", std)
# 分子 每一列都剪去其均值
numerator = arr - mean
print(numerator)
# 分母 标准差
denominator = std
result = numerator / denominator
print(result)
print(np.mean(result, axis=0))
print(np.std(result, axis=0))
"""
标准化的结果：
每一列的均值为0 np.mean(result, axis=0) = [0. 0. 0. 0.]
标准差为1 np.std(result, axis=0) = [1. 1. 1. 1.]
"""