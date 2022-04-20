class ProductionLine:
    """Iterator for list"""

    def __init__(self, product):
        self.product = product

    def __getitem__(self, index):
        return self.product[index]


if __name__ == '__main__':
    plan_list = ["model 1", "model S", "model G"]
    factory = ProductionLine(plan_list)
    for item in factory:
        print(item, end=", ")
    print()
    print(factory[:2])
    shop_list = ["model S", "model V"]
    shop_list.extend(factory)
    print(shop_list)

