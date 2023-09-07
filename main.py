from pyray import *
import random

from raylib import KEY_R

empty = -1
O = 0
X = 1

windowsize = 750

init_window(windowsize, windowsize, b"TicTacToe")
set_target_fps(60)

obamagreen = Color()
obamagreen.r = 240
obamagreen.g = 248
obamagreen.b = 215
obamagreen.a = 255

squares = [[empty, empty, empty],
           [empty, empty, empty],
           [empty, empty, empty]]

turn = [X, O][random.randint(0, 1)]

# Define the draw_board function to draw the lines of the board
def draw_board():
    draw_line_ex(Vector2(150, 150*2), Vector2(150*4, 150*2), 3, YELLOW)
    draw_line_ex(Vector2(150, 150*3), Vector2(150*4, 150*3), 3, YELLOW)
    draw_line_ex(Vector2(150*2, 150), Vector2(150*2, 150*4), 3, YELLOW)
    draw_line_ex(Vector2(150*3, 150), Vector2(150*3, 150*4), 3, YELLOW)

# Define the draw_squares function to draw the X and O symbols
def draw_squares():
    for i in range(0, 3):
        for j in range(0, 3):
            if squares[i][j] == empty:
                pass
            elif squares[i][j] == O:
                draw_circle(225+150*j, 225+150*i, 75, WHITE)
            else:
                draw_line_ex(Vector2(150+150*j, 150+150*i), Vector2(150*2+150*j, 150*2+150*i), 3, ORANGE)
                draw_line_ex(Vector2(150*2+150*j, 150+150*i), Vector2(150+150*j, 150*2+150*i), 3, ORANGE)

# Define the draw_top_text function to display the player's turn
def draw_top_text(text):
    draw_text(text, 50, 50, 20, obamagreen)

# Define the get_mouse_square function to get the row and column of the clicked square
def get_mouse_square():
    mp = get_mouse_position()
    if mp.x > 150 and mp.y > 150 and mp.x < 4*150 and mp.y < 4*150:
        row = int((mp.y - 150) / 150)
        col = int((mp.x - 150) / 150)
        return row, col
    return None, None

# Define the toggle_turn function to switch the player's turn
def toggle_turn():
    global turn
    turn = X if turn == O else O

# Define the check_win function to check for a win condition (implement this part)
def check_win():
    # Implement win condition checking here
    return False

# Define the game_over function to handle the game over screen (implement this part)
def game_over():
    # Implement game over screen handling here
    pass

# Main game loop
while not window_should_close():
    begin_drawing()
    clear_background(Color(48, 213, 200, 255))

    # Display whose turn it is
    draw_top_text("Player's Turn: X" if turn == X else "Player's Turn: O")

    # Draw the game board and squares using the draw_board and draw_squares functions
    draw_board()
    draw_squares()

    # Check for mouse click and update the board
    if is_mouse_button_down(0):
        row, col = get_mouse_square()
        if row is not None and col is not None and squares[row][col] == empty:
            squares[row][col] = turn
            toggle_turn()

    # Check for a win and handle the game over screen
    if check_win():
        game_over()

    end_drawing()

# Close the game window

# ... (previous code)

# Define a variable to keep track of whether the game is over and who the winner is
game_over = False
winner = None
winning_combination = []

# Define the find_winning_combination function to check for a win
def find_winning_combination():
    # Check rows
    for row in squares:
        if row[0] == row[1] == row[2] != empty:
            return [(squares.index(row), 0), (squares.index(row), 1), (squares.index(row), 2)]

    # Check columns
    for col in range(3):
        if squares[0][col] == squares[1][col] == squares[2][col] != empty:
            return [(0, col), (1, col), (2, col)]

    # Check diagonals
    if squares[0][0] == squares[1][1] == squares[2][2] != empty:
        return [(0, 0), (1, 1), (2, 2)]
    if squares[0][2] == squares[1][1] == squares[2][0] != empty:
        return [(0, 2), (1, 1), (2, 0)]

    return None


# Main game loop
while not window_should_close():
    begin_drawing()
    clear_background(Color(48, 213, 200, 255))

    if not game_over:
        # Display whose turn it is
        draw_top_text("Player's Turn: X" if turn == X else "Player's Turn: O")

        # Draw the game board and squares using the draw_board and draw_squares functions
        draw_board()
        draw_squares()

        # Check for mouse click and update the board only if the game is not over
        if is_mouse_button_down(0) and not game_over:
            row, col = get_mouse_square()
            if row is not None and col is not None and squares[row][col] == empty:
                squares[row][col] = turn
                toggle_turn()

        # Check for a win and handle the game over screen
        winning_combination = find_winning_combination()
        if winning_combination:
            game_over = True
            winner = "X" if turn == O else "O"
        elif all(squares[i][j] != empty for i in range(3) for j in range(3)):
            game_over = True
            winner = "Tie"

    else:
        # Display the winning combination
        if winning_combination:
            for row, col in winning_combination:
                draw_circle(225 + 150 * col, 225 + 150 * row, 10, RED)

        # Display the winner or tie and the option to play again
        if winner == "Tie":
            draw_top_text("It's a tie! Press " + str(KEY_R) + " to play again.")
        else:
            draw_top_text("Winner is Player " + winner + ". Press " + str(KEY_R) + " to play again.")

        # Check for rematch option (pressing the 'R' key)
        if is_key_pressed(KEY_R):
            # Reset the game state for a rematch
            squares = [[empty, empty, empty],
                       [empty, empty, empty],
                       [empty, empty, empty]]
            turn = [X, O][random.randint(0, 1)]
            game_over = False
            winner = None
            winning_combination = []

    end_drawing()

# Close the game window
close_window()






#def get_winning_combos():
#    rows = [[(move.row,move.col) for move in row]
#        for row in self._current_moves]
#    columns = [list(col) for col in zip(*rows)]
#    first_diagonal = [row[i] for i, row in enumerate(rows)]
#    second_diagonal = [col[j] for j, col in enumerate(reversed(columms))]
#    return rows + columns + [first_diagonal, second_diagonal]



    


#a thing that gets the mouse position and changes a square
#a turn tracker
#something to check if someone one
#game over screen
#text on top
#the stuff on the bottom
#local multiplayer
#online multiplayer
#against CPU
#leaderboard
#ADS TO MAKE MONEY
#NFT
#cryptomining
#SWIFT??







