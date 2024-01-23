from pyray import *
from raylib import KEY_R, KEY_Q, KEY_ONE, KEY_TWO, KEY_THREE, KEY_FOUR, KEY_FIVE, KEY_SIX, KEY_SEVEN, KEY_EIGHT, KEY_NINE, KEY_ZERO, KEY_PERIOD, KEY_BACKSPACE, KEY_ENTER


class Square:
    EMPTY = -1
    O = 0
    X = 1

class Player:
    O = 0
    X = 1
    



# Define the find_winning_combination function to check for a win
def find_winning_combination(squares):
    # Check rows
    for row in squares:
        if row[0] == row[1] == row[2] != Square.EMPTY:
            return [(squares.index(row), 0), (squares.index(row), 1), (squares.index(row), 2)]

    # Check columns
    for col in range(3):
        if squares[0][col] == squares[1][col] == squares[2][col] != Square.EMPTY:
            return [(0, col), (1, col), (2, col)]

    # Check diagonals
    if squares[0][0] == squares[1][1] == squares[2][2] != Square.EMPTY:
        return [(0, 0), (1, 1), (2, 2)]
    if squares[0][2] == squares[1][1] == squares[2][0] != Square.EMPTY:
        return [(0, 2), (1, 1), (2, 0)]
    
    return None




def game_logic(game):
    squares = game.squares
    draw_board()
    draw_squares(squares)
    #check if game is over, otherwise, ask for player move
    if game.game_quit:
        return True
    game_over = False
    winning_combination = find_winning_combination(squares)
    if winning_combination or all(squares[i][j] != Square.EMPTY
                                  for i in range(3)
                                  for j in range(3)):
        game_over = True
        
    if not game_over:
        my_turn = False
        turn = game.see_whos_turn_it_is()
        for player in game.human_players_here:
            if turn == player:
                my_turn = True
                break
        if my_turn:
            if is_mouse_button_pressed(0):
                row, col = get_mouse_square()
                if row is not None and col is not None and squares[row][col] == Square.EMPTY:
                    game.do_move(player, row * 3 + col + 1)#move is number from 1 to 9
        else:
            game.wait_for_other_player()
    return game_over

# Define the draw_board function to draw the lines of the board
def draw_board():
    draw_line_ex(Vector2(150, 150*2), Vector2(150*4, 150*2), 3, YELLOW)
    draw_line_ex(Vector2(150, 150*3), Vector2(150*4, 150*3), 3, YELLOW)
    draw_line_ex(Vector2(150*2, 150), Vector2(150*2, 150*4), 3, YELLOW)
    draw_line_ex(Vector2(150*3, 150), Vector2(150*3, 150*4), 3, YELLOW)

# Define the draw_squares function to draw the X and O symbols
def draw_squares(squares):
    for i in range(0, 3):
        for j in range(0, 3):
            if squares[i][j] == Square.EMPTY:
                pass
            elif squares[i][j] == Square.O:
                draw_circle(225+150*j, 225+150*i, 75, WHITE)
            else:
                draw_line_ex(Vector2(150+150*j, 150+150*i), Vector2(150*2+150*j, 150*2+150*i), 3, ORANGE)
                draw_line_ex(Vector2(150*2+150*j, 150+150*i), Vector2(150+150*j, 150*2+150*i), 3, ORANGE)


# Define the find_winning_combination function to check for a win
def find_winning_combination(squares):
    # Check rows
    for row in squares:
        if row[0] == row[1] == row[2] != Square.EMPTY:
            return [(squares.index(row), 0), (squares.index(row), 1), (squares.index(row), 2)]

    # Check columns
    for col in range(3):
        if squares[0][col] == squares[1][col] == squares[2][col] != Square.EMPTY:
            return [(0, col), (1, col), (2, col)]

    # Check diagonals
    if squares[0][0] == squares[1][1] == squares[2][2] != Square.EMPTY:
        return [(0, 0), (1, 1), (2, 2)]
    if squares[0][2] == squares[1][1] == squares[2][0] != Square.EMPTY:
        return [(0, 2), (1, 1), (2, 0)]
    
    return None


# Define the get_mouse_square function to get the row and column of the clicked square
def get_mouse_square():
    mp = get_mouse_position()
    if mp.x > 150 and mp.y > 150 and mp.x < 4*150 and mp.y < 4*150:
        row = int((mp.y - 150) / 150)
        col = int((mp.x - 150) / 150)
        return row, col
    return None, None

def game_over_screen(game):
    squares = game.squares
    winning_combination = find_winning_combination(squares)
    if winning_combination:
        for row, col in winning_combination:
            draw_circle(225 + 150 * col, 225 + 150 * row, 20, RED)
                
    # Display the winner or tie and the option to play again if the other player hasn't quit

    rematch_option_display =  " Press " + str(KEY_R) + " for a rematch." if not game.rematch_requested  or game.other_quit else " Rematch requested." if not game.other_quit else " Other player quit."
    
    if not winning_combination:
        draw_top_text("It's a tie." + rematch_option_display)
    else:
        row, col = winning_combination[0]
        winner = squares[row][col]
        if winner in game.human_players_here:
            draw_top_text(("Player {player} wins!" + rematch_option_display).format(player = "X" if winner == Player.X else "O"))
        else:
            draw_top_text("You lose." + rematch_option_display)

    draw_secondary_top_text("or press " + str(KEY_Q) + " to quit.")

    if is_key_pressed(KEY_R) and not game.other_quit and not game.rematch_requested:
        game.request_rematch()
    if is_key_pressed(KEY_Q):
        game.quit_game()

        

class Move:
    def __init__(self,player,position):
        self.player = player
        self.position = position
        
# Define the draw_top_text function to display the player's turn
def draw_top_text(text):
    draw_text(text, 50, 50, 20, obamagreen)
def draw_secondary_top_text(text):
    draw_text(text, 50, 100, 20, obamagreen)

obamagreen = Color()
obamagreen.r = 240
obamagreen.g = 248
obamagreen.b = 215
obamagreen.a = 255
