def test_var_args(f_arg, *args):
    print("first normal args: ", f_arg)
    for arg in args:
        print("another argument: ", arg)


"""
*args 是用来发送一个非键值对的可变数量的参数列表给一个函数
"""
test_var_args('golang', 'python', 'eggs', 'test')
"""
**kwargs 允许你将不定长度的键值对, 作为参数传递给一个函数。 
如果你想要在一个函数里处理带名字的参数, 你应该使用**kwargs
"""


def greet_me(**kwargs):
    for key, value in kwargs.items():
        print("{0} == {1}".format(key, value))


greet_me(name='cat', mark='🐱')

args = ['I', 'am', 'fine']


def blank_words(arg1, arg2, arg3):
    print(arg1, arg2, arg3)


blank_words(*args)

kwargs = {"arg1": "am", "arg2": "I", "arg3": "fine"}
blank_words(**kwargs)
