
NUMBER=9
columns = 0
row = 0
while ( row < NUMBER ):
    while (columns < NUMBER ):
        if row < NUMBER/2:
            if columns > (NUMBER/2-(row+1)) and\
                    columns <= (row + NUMBER/2):
                print("*"),
            else:
                print(" "),
        else:
            if columns >= ( row - NUMBER/2) and\
                    columns < ( NUMBER - (row-NUMBER/2)):
                print("*"),
            else:
                print(" "),
        columns = columns + 1
    print("")
    columns = 0 
    row = row + 1

