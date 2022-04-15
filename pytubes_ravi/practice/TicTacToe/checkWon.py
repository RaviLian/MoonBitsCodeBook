_table = [['X', 'O', 'O'],
          ['X', 'O', 'X'],
          ['O', 'X', 'X'], ]


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


print('O胜:', checkWon(_table, 'O'))
