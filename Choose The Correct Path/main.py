import random

GRID_SIZE = 10


BOMB_NUMBERS = []  # Example bomb numbers
for i in range(3):
    BOMB_NUMBERS.append(random.randint(1, 100))
    
EXIT_POS = (GRID_SIZE - 1, GRID_SIZE - 1)

def generate_grid(size):
    nums = list(range(1, size * size + 1))
    random.shuffle(nums)
    grid = [nums[i*size:(i+1)*size] for i in range(size)]
    return grid

def print_grid(grid, player_pos):
    for i, row in enumerate(grid):
        for j, num in enumerate(row):
            if (i, j) == player_pos:
                print("[*ME*]", end=" ")
            else:
                print(f"[{num}]", end=" ")
        print()
    print()

def find_number_pos(grid, number):
    for i, row in enumerate(grid):
        for j, num in enumerate(row):
            if num == number:
                return (i, j)
    return None

def main():
    grid = generate_grid(GRID_SIZE)
    player_pos = (0, 0)
    print("Welcome to the Grid Game!")
    print("Move using W/A/S/D. Reach the bottom-right corner. Avoid bombs!")
    while True:
        print_grid(grid, player_pos)
        i, j = player_pos
        num = grid[i][j]
        if num in BOMB_NUMBERS:
            print(f"Boom! You stepped on a bomb ({num}). Restarting...")
            player_pos = (0, 0)
            continue
        if player_pos == EXIT_POS:
            print("Congratulations! You reached the exit safely!")
            break
        move = input("Move (W/A/S/D): ").strip().upper()
        if move == 'W' and i > 0:
            player_pos = (i-1, j)
        elif move == 'S' and i < GRID_SIZE-1:
            player_pos = (i+1, j)
        elif move == 'A' and j > 0:
            player_pos = (i, j-1)
        elif move == 'D' and j < GRID_SIZE-1:
            player_pos = (i, j+1)
        else:
            print("Invalid move!")

if __name__ == "__main__":
    main()