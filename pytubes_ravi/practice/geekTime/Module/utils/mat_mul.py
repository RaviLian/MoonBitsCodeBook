from geekTime.Module.proto.mat import Matrix


def mat_mul(matrix_1: Matrix, matrix_2: Matrix):
    assert matrix_1.m == matrix_2.n
    n, m, s = matrix_1.n, matrix_1.m, matrix_2.m
    result = [[0 for _ in range(n)] for _ in range(s)]
    for i in range(n):
        for j in range(s):
            for k in range(m):
                result[i][k] += matrix_1.data[i][j] * matrix_2.data[j][k]

    return Matrix(result)


# import时不会暴露这段代码，用于模块化的测试
if __name__ == '__main__':
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])

    print(mat_mul(a, b).data)
