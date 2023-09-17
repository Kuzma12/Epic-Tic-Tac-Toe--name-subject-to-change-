from pyray import *
import random
import socket
import time

from raylib import KEY_R, KEY_ONE, KEY_TWO, KEY_THREE, KEY_FOUR, KEY_FIVE, KEY_SIX, KEY_SEVEN, KEY_EIGHT, KEY_NINE, KEY_ZERO, KEY_PERIOD, KEY_BACKSPACE, KEY_ENTER

empty = -1
O = 0
X = 1

windowsize = 750

init_window(windowsize, windowsize, b"TicTacToe")
set_target_fps(60)

squares = [[empty, empty, empty],
           [empty, empty, empty],
           [empty, empty, empty]]

turn = [X, O][random.randint(0, 1)]


main_menu = 0
local_multiplayer = 1
online_multiplayer = 2


game_mode = main_menu


obamagreen = Color()
obamagreen.r = 240
obamagreen.g = 248
obamagreen.b = 215
obamagreen.a = 255




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

drawn_once = False
def multiplayer_mode():
    global game_over
    global winner
    global turn
    global player
    global squares
    global c
    global winning_combination
    global drawn_once
    if not game_over:
        # Display whose turn it is
        draw_top_text("Player's Turn: X" if turn == X else "Player's Turn: O")
        draw_text(b'You are player' + (b'O' if player == O else b'X'), 150, 100, 40, WHITE)        
        # Draw the game board and squares using the draw_board and draw_squares functions
        draw_board()
        draw_squares()
        if turn == player:
            # Check for mouse click and update the board only if the game is not over
            if is_mouse_button_pressed(0) and not game_over:
                row, col = get_mouse_square()
                if row is not None and col is not None and squares[row][col] == empty:
                    squares[row][col] = turn
                    toggle_turn()
                    c.send(str(row * 3 + col).encode())
                    print("sent" + str(row * 3 + col))
                    drawn_once = False
        elif not drawn_once:
            draw_board()
            draw_squares()
            drawn_once = True
        else:

            response = c.recv(1024)
            print("recieved" + str(response.decode('utf-8')))
            move = int(response.decode('utf-8'))
            squares[move // 3][move % 3] = turn
            toggle_turn()

        # Check for a win and handle the game over screen
        winning_combination = find_winning_combination()
        if winning_combination:
            c.close()
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



def display_local_multiplayer():
    global game_over
    global winner
    global squares
    global turn
    global winning_combination
    if not game_over:
        # Display whose turn it is
        draw_top_text("Player's Turn: X" if turn == X else "Player's Turn: O")

        # Draw the game board and squares using the draw_board and draw_squares functions
        draw_board()
        draw_squares()

        # Check for mouse click and update the board only if the game is not over
        if is_mouse_button_pressed(0) and not game_over:
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




            
def display_main_menu():
    global game_mode
    
    def game_mode_selection():
        mp = get_mouse_position()
        if mp.x > 150 and mp.y > 150 and mp.x < 4*150 and mp.y < 2*150:
            return local_multiplayer
        elif mp.x > 150 and mp.y > 150 * 3 and mp.x < 4*150 and mp.y < 4*150:
            return online_multiplayer
        else:
            return None
        
        
    draw_text(b"Welcome to EPIC TIC TAC TOE (name subject to change)", 150, 50, 20, WHITE)

    draw_rectangle(150, 150, 150*3, 150, WHITE)
    draw_text(b"Local Multiplayer", 150, 150, 50, ORANGE)

    draw_rectangle(150, 3*150, 150*3, 150, WHITE)            
    draw_text(b"Online Multiplayer", 150, 3*150, 50, ORANGE)

    if is_mouse_button_down(0) and game_mode_selection() is not None:
        game_mode = game_mode_selection()

        
host = 0
client = 1

host_or_client = None

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
        return IP

join_code = b''

def generate_join_code():
    return str.encode(get_ip())
player = None
s = None
c = None
game_started = False

def host_mode():
    global join_code
    global s
    global c
    global turn
    global player
    global game_started
    if c == None:
        if turn == X:
            draw_text(b"You are player X", 150, 150, 30, ORANGE)
        else:
            draw_text(b"You are player O", 150, 150, 30, ORANGE)
    
        join_code = generate_join_code()
        draw_text(b"Your join code is " + join_code, 150, 3*150, 30, ORANGE)
    
        if s == None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('',12345))
        else:
            s.listen(5)
            print ("socket is listening")
            c, addr = s.accept()
            print ('Got connection from', addr)

    elif not game_started:
        time.sleep(2)
        c.send(("You are player " + ("O" if turn == X else "X")).encode())
        player = turn
        game_started = True
    else:
        multiplayer_mode()

        
class IPKeys:
    ZERO = KEY_ZERO
    ONE = KEY_ONE
    TWO = KEY_TWO
    THREE = KEY_THREE
    FOUR = KEY_FOUR
    FIVE = KEY_FIVE
    SIX = KEY_SIX
    SEVEN = KEY_SEVEN
    EIGHT = KEY_EIGHT
    NINE = KEY_NINE
    DOT = KEY_PERIOD
    BS = KEY_BACKSPACE
    ENTER = KEY_ENTER
        
                
    
def client_mode():
    global join_code
    global player
    global turn
    global s
    global c
    global game_started
    if not game_started:
        draw_text(b"Enter Join Code then push enter (Numbers 0-9 and dot (.):", 150, 150, 30, ORANGE)
        draw_text(b"Join Code:" + join_code, 150, 4*150, 30, ORANGE)
        match get_key_pressed():
            case IPKeys.ZERO:
                join_code += b'0'
            case IPKeys.ONE:
                join_code += b'1'
            case IPKeys.TWO:
                join_code += b'2'
            case IPKeys.THREE:
                join_code += b'3'
            case IPKeys.FOUR:
                join_code += b'4'
            case IPKeys.FIVE:
                join_code += b'5'
            case IPKeys.SIX:
                join_code += b'6'
            case IPKeys.SEVEN:
                join_code += b'7'
            case IPKeys.EIGHT:
                join_code += b'8'
            case IPKeys.NINE:
                join_code += b'9'
            case IPKeys.DOT:
                join_code += b'.'
            case IPKeys.BS:
                join_code = join_code.decode('utf-8')
                join_code = join_code[0:len(join_code) - 2]
                join_code = join_code.encode()
            case IPKeys.ENTER:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                IP = join_code.decode('utf-8')
                print("CONNECTING" + IP)
                s.connect((IP,12345))
                print("CONNECTED")
                response = (s.recv(1024)).decode('utf-8')
                print(response)
                player = X if response[15] == 'X' else O
                print(response[15])
                turn = O if player == X else X
                c = s
                game_started = True
    else:
        multiplayer_mode()








def display_online_multiplayer():
    def ask_to_be_host_or_client():
        global host_or_client
        def mode_selection():
            mp = get_mouse_position()
            if mp.x > 150 and mp.y > 150 and mp.x < 4*150 and mp.y < 2*150:
                return host
            elif mp.x > 150 and mp.y > 150 * 3 and mp.x < 4*150 and mp.y < 4*150:
                return client
            else:
                return None
            
        draw_text(b"Do you want to be the host or client?", 150, 50, 20, WHITE)

        draw_rectangle(150, 150, 150*3, 150, WHITE)
        draw_text(b"Host", 150, 150, 50, ORANGE)

        draw_rectangle(150, 3*150, 150*3, 150, WHITE)            
        draw_text(b"Client", 150, 3*150, 50, ORANGE)
        if is_mouse_button_pressed(0) and mode_selection() is not None:
            host_or_client = mode_selection()

        
    if host_or_client is None:
        ask_to_be_host_or_client()
    elif host_or_client == host:
        host_mode()
    else:
        client_mode()
    
    





    
# Main game loop
while not window_should_close():
    begin_drawing()
    clear_background(Color(48, 213, 200, 255))

    if game_mode == main_menu:
        display_main_menu()
    elif game_mode == local_multiplayer:
        display_local_multiplayer()
    else:
        display_online_multiplayer()


    
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
