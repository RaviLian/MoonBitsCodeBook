from collections import namedtuple

user_tuple = ("S100101", "Ravi", 1, "18811238681", "湖北省武汉市")

customer_id, name, *others = user_tuple

print(customer_id)
print(name)
print(type(others), others)

def handle_num(num):
    if num > 15:
        elem = num * num / 10 * 2
    elif num > 20:
        elem = num / 20 % 5
    else:
        elem = -num
    return elem

# 列表生成式性能优于列表操作
l = [(i, handle_num(i)) for i in range(15, 30) if i % 2 == 0]
print(l)

vals = ['j', 'k', 'o', 'ppl', 'ppl2']
# 字典推导式
d = {k: v for k, v in enumerate(vals)}
print(d)

"""named"""
Patient = namedtuple("Patient", ['pid', 'name', 'sex', 'phone', 'plan_id'])
p_dict = {
    'pid': 'S01',
    'name': 'jack',
    'sex': 1,
    'phone': '11093174',
}
# 构建简单对象
p = Patient(**p_dict, plan_id=2)
print(p.name)

# dict
uu = ['l1', 'l2', 'l1', 'l3', 'l2']
ddd = {}
for u in uu:
    if u not in ddd:
        ddd[u] = 1
    else:
        ddd[u] += 1
print(ddd)

from collections import defaultdict

ddt = defaultdict(int)
for u in uu:
    # key 不存在默认创建key，val赋值为0
    ddt[u] += 1
print(ddt)
