import time
import random
import math

def print_board(board):
    RED = "\033[31m"
    BLACK = "\033[37m"
    
    N = len(board)
    n = math.floor(math.sqrt(N))
    assert N == n*n

    board_string = ""
    for row in range(N):
        if row > 0 and row % n == 0:
            board_string += "\n"
        for col in range(N):
            if col > 0 and col % n == 0: 
                board_string += " "
            value = board[row][col]
            if value != 0:
                board_string += RED
            else:
                board_string += BLACK
            board_string += "[{:02.0f}]".format(value)
            
        board_string += "\n" + BLACK

    print(board_string)

def regValueHelper(row,col, board):
    board_size = int(math.sqrt(len(board)))
    reg_row = row // board_size
    reg_col = col // board_size
    return reg_row * board_size + reg_col

def make_puzzle(N):
    board = []

    for _ in range(N):
        empty = []
        for _ in range(N):
            empty.append(0)
        board.append(empty)
    row_sets = []
    for _ in range(N):
        row_sets.append(set())
    col_sets = []
    for _ in range(N):
        col_sets.append(set())
    reg_sets = []
    n = int(math.sqrt(N))
    for _ in range(n*n):
        reg_sets.append(set())

    row = set()
    for row1 in board:
        for row1 in row:
            row.add(row1)
    col = set()
    for col1 in board:
        for col1 in col:
            col.add(col1)

    for _ in range(1,n):
        col.add(random.randrange(0,len(board)-1))

    puzzle = {'board':board,'row_sets':row_sets,'col_sets':col_sets,'reg_sets':reg_sets}
    return puzzle

def get_square(puzzle,row,col):
    value = puzzle.get('board')[row][col]
    row_set = puzzle.get('row_sets')[row]
    col_set = puzzle.get('col_sets')[col]
    board = puzzle.get('board')
    reg_set = puzzle.get('reg_sets')[regValueHelper(row,col,board)]
    square_dict =  {'value':value,'row_set':row_set,'col_set':col_set,'reg_set':reg_set}
    return square_dict

def move(puzzle,row,col,new_value):
    puzzle_info = get_square(puzzle,row, col)
    if new_value in puzzle_info.get('row_set') or new_value in puzzle_info.get('col_set') or new_value in puzzle_info.get('reg_set'):
            return False
    if puzzle_info.get('value') == 0:
        puzzle["board"][row][col]=new_value
        puzzle['row_sets'][row].add(new_value)
        puzzle['col_sets'][col].add(new_value)
        puzzle['reg_sets'][regValueHelper(row,col,puzzle.get('board'))].add(new_value)
        return True
    else:
        return False
def fill_puzzle(puzzle):
    n = 0
    length = len(puzzle['board'])
    while n <= length**4:
        row = random.randint(0,len(puzzle['board'])-1)
        col = random.randint(0,len(puzzle['board'])-1)
        new_value = random.randint(1,len(puzzle['board']))
        move(puzzle,row,col,new_value)
        n +=1
    print()
    
def main():
        
    start_time = time.time()
    N = 16
    print("Board size:", N, "x", N)
    puzzle = make_puzzle(N)
    print("Initial puzzle:")
    print(puzzle)
    print("Initial board:")
    print_board(puzzle['board'])
    fill_puzzle(puzzle)
    print_board(puzzle['board'])
    count = 0
    total = N*N
    for row in range(N):
        for col in range(N):
            if puzzle['board'][row][col]!=0:
                count += 1
    percentage = (count/total)*100
    print(percentage, 'percent of the board is filled')
    print(fill_puzzle)
    print("Elapsed time to fill the board:","---%s seconds---"%(time.time() - start_time))

main()
