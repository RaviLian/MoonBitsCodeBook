from typing import List


def myfunc(num_list: List[int]) -> str:
    """调换首尾元素"""
    assert len(num_list) >= 2
    num_list[0], num_list[-1] = num_list[-1], num_list[0]
    return "num_list"


print(myfunc([9, 8]))
print(help(myfunc))
print(type(myfunc))