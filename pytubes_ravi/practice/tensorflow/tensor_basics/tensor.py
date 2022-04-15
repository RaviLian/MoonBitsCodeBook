import os
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# print(tf.__version__)
# Initialization of Tensors
x = tf.constant(4, shape=(1, 1), dtype=tf.float64)
# 2 * 3 matrix
x = tf.constant([[1, 2, 3], [4, 5, 6]])
x = tf.zeros((2, 3))
# Identity matrix
x = tf.eye(3, dtype=tf.int64)
x = tf.random.normal((3, 3), mean=0, stddev=1)
x = tf.random.uniform((1, 3), minval=0, maxval=1)
x = tf.range(start=1, limit=20, delta=2.5, dtype=tf.float64)
# 直接舍去小数点
x = tf.cast(x, dtype=tf.int64)

# Mathematical Operations
x = tf.constant([1, 2, 3])
y = tf.constant([8, 9, 10])
z = tf.add(x, y)  # z = x + y
z = y - x
z = y / x
z = tf.tensordot(x, y, axes=1)

x = tf.random.normal((2, 3))
y = tf.random.normal((3, 4))
z = x @ y

# Indexing
x = tf.constant([0, 1, 2, 2, 4, 5, 6, 7, 8])
# print(x[::2])  # 两步走
# print(x[::-1])  # 倒叙打印

indices = tf.constant([0, 3])
x_ind = tf.gather(x, indices)
# print(x_ind)  # 得到索引下的值

x = tf.constant([[1, 2],
                 [3, 4],
                 [5, 6]])
# print(x[0, :]) # 获取第一行全部
# print(x[0:2, :])  # 获取前两行全部

# Reshaping
x = tf.range(9)
x = tf.reshape(x, (3, 3))
print(x)

# x = tf.transpose(x, perm=[0, 1])
x = tf.transpose(x, perm=[1, 0])
print(x)