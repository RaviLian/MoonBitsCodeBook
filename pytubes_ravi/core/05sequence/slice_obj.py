from collections import abc
import numbers

class Group:
    def __init__(self, group_name, root_name, items):
        self.group_name = group_name
        self.root_name = root_name
        self.items = items

    def __reversed__(self):
        pass

    def __getitem__(self, item):
        """实现切片的关键"""
        cls = type(self)
        if isinstance(item, slice):
            return cls(group_name=self.group_name,
                       root_name=self.root_name, items=self.items[item])
        elif isinstance(item, numbers.Integral):
            return  cls(group_name=self.group_name,
                        root_name=self.root_name, items=[self.items[item]])  # 改成数组

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, item):
        if item in self.items:
            return True
        else:
            return False


if __name__ == '__main__':
    li = [1, 2, 3, 4]
    g = Group("nature_nums", "nums", li)
    sub_g = g[:2]
    sin_g = g[3]
    if 4 in g:
        print("yeah")
