import random
import time

board = [[]]
board_size = 10
num_of_ships = 5
bullets_left = 50
game_over = False
num_of_ships_sunk = 0
ship_positions = [[]]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# creating the board
def create_board():
    global board
    global board_size
    global num_of_ships
    global ship_positions
    random.seed(time.time())

    rows, cols = [board_size, board_size]

    board = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append('.')
        board.append(row)

    num_of_ships_placed = 0

    ship_positions = []

    while num_of_ships_placed != num_of_ships:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.choice([2, 3, 3, 4, 5])
        if try_to_place_ship_on_board(random_row, random_col, direction, ship_size):
            num_of_ships_placed += 1


def validate_board_and_place_ship(start_row, end_row, start_col, end_col):
    global board
    global ship_positions

    all_valid = True

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[r][c] != ".":
                all_valid = False
                break
    if all_valid:
        ship_positions.append([start_row, end_row, start_col, end_col])
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                board[r][c] = "O"
    return all_valid


def try_to_place_ship_on_board(row, col, direction, length):
    global board_size

    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
    if direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1

    elif direction == "right":
        if col + length > board_size:
            return False
        end_col = col + length

    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1

    elif direction == "down":
        if row + length > board_size:
            return False
        end_row = row + length

    return validate_board_and_place_ship(start_row, end_row, start_col, end_col)


def print_board():
    global board
    global alphabet

    debug_mode = False

    alphabet = alphabet[0: len(board) + 1]

    for row in range(len(board)):
        print(alphabet[row], end=" ")
        for col in range(len(board[row])):
            if board[row][col] == "O":
                if debug_mode:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(board[row][col], end=" ")
        print("")

    print(" ", end=" ")
    for i in range(len(board[0])):
        print(str(i), end=" ")
    print("")


def accept_valid_bullet_placement():
    global alphabet
    global board

    is_valid_placement = False
    row = -1
    col = -1

    while is_valid_placement is False:
        placement = input("Enter row (A-J) and column (0-9) such as A0: ")
        placement = placement.upper()
        if len(placement) <= 0 or len(placement) > 2:
            print("Error: enter a standard input")
            continue
        row = placement[0]
        col = placement[1]
        if not row.isalpha() or not col.isnumeric():
            print("Error: enter a standard input")
            continue
        row = alphabet.find(row)
        if not (-1 < row < board_size):
            print("Error: enter a standard input")
            continue
        col = int(col)
        if not (-1 < col < board_size):
            print("Error: enter a standard input")
            continue
        if board[row][col] == "#" or board[row][col] == "X":
            print("You have already shot a bullet here")
            continue
        if board[row][col] == "O" or board[row][col] == ".":
            is_valid_placement = True

    return row, col


def ship_sunk_check(row, col):
    for position in ship_positions:
        start_row = position[0]
        end_row = position[1]
        start_col = position[2]
        end_col = position[3]
        if start_row <= row <= end_row and start_col <= col <= end_col:
            for r in range(start_row, end_row):
                for c in range(start_col, end_col):
                    if board[r][c] != "X":
                        return False
    return True


def shoot_bullet():
    global board
    global num_of_ships_sunk
    global bullets_left

    row, col = accept_valid_bullet_placement()
    print("")
    print("----------------------------------")

    if board[row][col] == ".":
        print("You missed it")
        board[row][col] = "#"
    elif board[row][col] == "O":
        print("You hit!", end=" ")
        board[row][col] = "X"
        if ship_sunk_check(row, col):
            print("Ship has completely sunk!!")
            num_of_ships_sunk += 1
        else:
            print("Ship was shot")
    bullets_left -= 1


def check_game_over():
    global num_of_ships_sunk
    global num_of_ships
    global bullets_left
    global game_over
    global board
    global alphabet

    if num_of_ships == num_of_ships_sunk:
        print("Congrats you won!!!")
        game_over = True
    elif bullets_left <= 0:
        print("Sorry, you ran out of bullets. Better luck next time!")
        print("Number of ships sunk: " + str(num_of_ships_sunk))
        game_over = True

        debug_mode = True

        alphabet = alphabet[0: len(board) + 1]

        for row in range(len(board)):
            print(alphabet[row], end=" ")
            for col in range(len(board[row])):
                if board[row][col] == "O":
                    if debug_mode:
                        print("O", end=" ")
                    else:
                        print(".", end=" ")
                else:
                    print(board[row][col], end=" ")
            print("")

        print(" ", end=" ")
        for i in range(len(board[0])):
            print(str(i), end=" ")
        print("")


def main():
    global game_over

    print("Welcome to BATTLESHIPS")
    print("You have 50 bullets to take down 5 ships. Lets begin! Best of Luck!!")

    create_board()

    while game_over is False:
        print_board()
        print("Number of ships remaining: " + str(num_of_ships - num_of_ships_sunk))
        print("Number of bullets left: " + str(bullets_left))
        shoot_bullet()
        print("----------------------------------")
        print("")
        check_game_over()

if __name__ == '__main__':
    main()
