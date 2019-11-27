from random import randint
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

index=0;
while index <  len(queens):
    queens[index] = randint(0,7)
    index= index+1


print queens

draw_board()


