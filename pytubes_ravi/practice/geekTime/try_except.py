# 当程序中存在多个 except block 时，最多只有一个 except block 会被执行。
# 换句话说，如果多个 except 声明的异常类型都与实际相匹配，
# 那么只有最前面的 except block 会被执行，其他则被忽略。
try:
    s = input('please enter two numbers separated by comma: ')
    s = s.split(',')
    num1 = int(s[0].strip())
    num2 = int(s[1].strip())
# 因为类型转换而报错
# except (ValueError, IndexError) as err:
except ValueError as err:
    print('Value Error: {}'.format(err))
except IndexError as err:
    print('IndexError Error: {}'.format(err))
# Exception 是其他所有非系统异常的基类，能够匹配任意非系统异常
except Exception as err:
    print('Other error: {}'.format(err))

print('continue')