# 全局变量保存棋盘
_table = [['.', '.', '.'],
          ['.', '.', '.'],
          ['.', '.', '.'], ]


# 打印棋盘
def print_table(table):
    for i in range(len(table)):
        for elem in table[i]:
            print(elem, end=' ')
        print()


# 检查落子处是否为空
def checkEmpty(x, y):
    if _table[x][y] != '.':
        return False
    return True


# 落子操作
def take_a_step(x, y, symbol):
    if x < 0 or y < 0:
        print("非法位置！")
        return
    if x > 2 or y > 2:
        print("非法位置!")
        return

    if checkEmpty(x, y):
        _table[x][y] = symbol
    else:
        print("您所下的位置已经有棋子了！")
        return


# 检查棋盘是否已经满了，为平局做准备
def checkTableFull(table):
    flag = True
    for line in table:
        for j in line:
            if j == '.':
                flag = False
                break
    return flag


# 检查是否胜利
def checkWon(table, symbol):
    success = (
        ((0, 0), (0, 1), (0, 2),),
        ((1, 0), (1, 1), (1, 2),),
        ((2, 0), (2, 1), (2, 2),),

        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

        ((0, 0), (1, 1), (2, 2)),
        ((2, 0), (1, 1), (0, 2)),
    )
    for line in success:
        x1, y1 = line[0]
        x2, y2 = line[1]
        x3, y3 = line[2]
        if table[x1][y1] == symbol \
                and table[x2][y2] == symbol \
                and table[x3][y3] == symbol:
            return True


# 获取输入
def get_input():
    s = input("请输入您要下的坐标：")
    x = s[0]
    y = s[2]
    x = int(x) - 1
    y = int(y) - 1
    symbol = input("请输入您的棋子：")
    return x, y, symbol


def main():
    while True:
        print_table(_table)
        x, y, symbol = get_input()
        take_a_step(x, y, symbol)
        if checkTableFull(_table):
            print_table(_table)
            print("棋盘已满！平局！游戏结束！")
            break
        if checkWon(_table, 'X'):
            print_table(_table)
            print("X胜！游戏结束！")
            break
        if checkWon(_table, 'O'):
            print_table(_table)
            print("O胜！游戏结束！")
            break


if __name__ == '__main__':
    main()
