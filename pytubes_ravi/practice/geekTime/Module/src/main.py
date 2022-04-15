import sys

from geekTime.Module.proto.mat import Matrix
from geekTime.Module.utils.mat_mul import mat_mul

a = Matrix([[1, 2], [3, 4]])
b = Matrix([[5, 6], [7, 8]])

print(mat_mul(a, b).data)
print(sys.path)
# Pycharm 做的一件事，就是将第一项设置为项目根目录的绝对地址
# 这样便可以使用绝对路径引入模块
