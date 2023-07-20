import random

# Game constants
BOARD_SIZE = 10  
CONNECT_LENGTH = 5

def print_board(board):
    # Print column numbers
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))  
    print()
    
    # Print board
    for i, row in enumerate(board):
        print(str(i) + " " + " ".join(row))  
    print()

def check_win(board, row, col, symbol):

    # Check row
    count = 0
    for i in range(max(col-CONNECT_LENGTH+1, 0), min(col+1, BOARD_SIZE)):
        if board[row][i] == symbol:
            count += 1
        else:
            count = 0
        if count == CONNECT_LENGTH:
            return True
    
    # Check column
    count = 0
    for i in range(max(row-CONNECT_LENGTH+1, 0), min(row+1, BOARD_SIZE)):
        if board[i][col] == symbol:
            count += 1
        else:
            count = 0
        if count == CONNECT_LENGTH:
            return True   

    # Check diagonals
    count = 0
    for offset in range(-CONNECT_LENGTH+1, CONNECT_LENGTH):
        i = row + offset
        j = col + offset
        if i >= 0 and i < BOARD_SIZE and j >= 0 and j < BOARD_SIZE:
            if board[i][j] == symbol:
                count += 1
            else:
                count = 0
            if count == CONNECT_LENGTH:
                return True

    count = 0
    for offset in range(-CONNECT_LENGTH+1, CONNECT_LENGTH):
        i = row + offset
        j = col - offset
        if i >= 0 and i < BOARD_SIZE and j >= 0 and j < BOARD_SIZE:
            if board[i][j] == symbol:
                count += 1
            else:
                count = 0
            if count == CONNECT_LENGTH:
                return True

    return False
        
# Get valid row/column input
def get_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if 0 <= value < BOARD_SIZE:
                return value
            else:
                print("Invalid position. Please enter 0-", BOARD_SIZE-1)
        except ValueError:
            print("Invalid input. Please enter a number.")

# AI to select strategic move or random valid move       
def ai_move(board):
    
    # Define a helper function to check if a move creates or blocks a line of five pieces
    def check_move(board, row, col, symbol):
        
        # Check if the position is empty
        if board[row][col] != " ":
            return False
        
        # Make a copy of the board and place the symbol on the position
        new_board = [row[:] for row in board]
        new_board[row][col] = symbol
        
        # Check if the move results in a win or blocks a win for either player
        return check_win(new_board, row, col, symbol) or check_win(new_board, row, col, opposite(symbol))
    
    # Define a helper function to get the opposite symbol of a given symbol
    def opposite(symbol):
        if symbol == "X":
            return "O"
        else:
            return "X"
    
    # Get the list of possible moves for the current board state
    possible_moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == " ":
                possible_moves.append((i, j))
    
    # If there are no possible moves, return None
    if not possible_moves:
        return None, None
    
    # Loop through all the possible moves and look for moves that create or block a line of five pieces
    strategic_moves = []
    for move in possible_moves:
        if check_move(board, move[0], move[1], "O"):
            strategic_moves.append(move)
    
    # If there are any strategic moves, choose one randomly and return it
    if strategic_moves:
        i, j = random.choice(strategic_moves)
        return i, j
    
    # Otherwise, choose a random valid move and return it
    else:
        i, j = random.choice(possible_moves)
        return i, j
    
def main():
    board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    current_player = "X"
    
    while True:
        print_board(board)
        
        if current_player == "X":
            # Human's turn
            row = get_input(f"{current_player}'s turn to choose a row: ")
            col = get_input(f"{current_player}'s turn to choose a column: ")
        else:
            # AI's turn
            row, col = ai_move(board)
            
        if board[row][col] != " ":
            print("Position occupied!")
            continue
        
        board[row][col] = current_player
        
        if check_win(board, row, col, current_player):
            print(f"{current_player} wins!")
            break
        
        # Toggle player
        if current_player == "X":
            current_player = "O" 
        else:
            current_player = "X"

if __name__ == "__main__":
    main()
