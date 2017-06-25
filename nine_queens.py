
SIZE = 8

queens = [1,2,3,4,5,6,7,8]

def draw_board():
    column = 0
    row = 0
    while(row < SIZE ):
        while(column < SIZE ):
            if row == queens[column]:
                print("x"),
            else:
                print("_"),
            column = column + 1
        print
        column = 0
        row = row +1

draw_board()
queens = [1,2,3,2,5,3,7,1]
print
draw_board()


