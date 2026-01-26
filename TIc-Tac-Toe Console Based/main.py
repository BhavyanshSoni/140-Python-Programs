import random

# Tic-Tac-Toe Game

# Function to print the Tic-Tac-Toe board
def print_board(board):
    print("---------")
    for row in board:
        print("|", " | ".join(row), "|")
    print("---------")

# Function to check if a player has won
def check_win(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all([cell == player for cell in board[i]]):  # Check rows
            return True
        if all([board[j][i] == player for j in range(3)]):  # Check columns
            return True
    if all([board[i][i] == player for i in range(3)]):  # Check diagonal 1
        return True
    if all([board[i][2 - i] == player for i in range(3)]):  # Check diagonal 2
        return True
    return False

# Function to check if the board is full
def check_full(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        
        # Get player input with exception handling
        valid_move = False
        while not valid_move:
            if current_player == "X":  # Human player's turn
                try:
                    # Get row and column from user input
                    row, col = input(f"Enter row and column (1-3) for {current_player}: ").split()
                    
                    # Convert inputs to integers and adjust for 0-indexed grid
                    row, col = int(row) - 1, int(col) - 1

                    # Check if the input is within bounds
                    if row not in range(3) or col not in range(3):
                        print("Invalid input. Row and column must be between 1 and 3.")
                        continue

                    # Check if the cell is already occupied
                    if board[row][col] != " ":
                        print("This cell is already occupied. Please choose another one.")
                        continue

                    # Place the player's mark
                    board[row][col] = current_player
                    valid_move = True
                except ValueError:
                    print("Invalid input. Please enter two numbers separated by a space.")
            else:  # Computer's turn
                row, col = random.randint(0, 2), random.randint(0, 2)
                if board[row][col] == " ":
                    board[row][col] = current_player
                    valid_move = True
        
        # Check if the current player has won
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        # Check if the board is full (tie game)
        if check_full(board):
            print_board(board)
            print("It's a tie!")
            break
        
        # Switch to the next player
        current_player = "O" if current_player == "X" else "X"

# Start the game
play_game()