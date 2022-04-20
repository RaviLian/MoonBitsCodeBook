from collections.abc import Sized


class ProductionLine:
    """Iterator for list"""

    def __init__(self, product):
        self.product = product

    def __getitem__(self, index):
        return self.product[index]

    def __len__(self):
        return len(self.product)


if __name__ == '__main__':
    fac = ProductionLine([1, 2, 3, 4])
    print(hasattr(fac, "__len__"))  # 检查是否含有该属性
    # 希望某个类强制实现某个方法
    print(isinstance(fac, Sized))
