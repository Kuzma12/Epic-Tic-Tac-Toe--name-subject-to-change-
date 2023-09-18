from pyray import *
import random
import socket
import time
import threading
import queue

from raylib import KEY_R, KEY_Q, KEY_ONE, KEY_TWO, KEY_THREE, KEY_FOUR, KEY_FIVE, KEY_SIX, KEY_SEVEN, KEY_EIGHT, KEY_NINE, KEY_ZERO, KEY_PERIOD, KEY_BACKSPACE, KEY_ENTER


class Square:
    EMPTY = -1
    O = 0
    X = 1

class TwoWayConnection:
    def __init__(self,IP,Port,is_host):
        self.should_end = False
        self.ip= IP
        self.port = Port
        self.inbox = queue.Queue()
        self.outbox = queue.Queue()
        self.c1 = None
        self.c2 = None
        self.s = None
        self.is_host = is_host
        threading.Thread(target=lambda : self.make_connections()).start()
        self.outbox_thread = threading.Thread(target=self.send_messages)
        self.inbox_thread = threading.Thread(target=self.receive_messages)
    def secret_message():
        return str(random.randint(0,120)).encode()
    def make_connections(self):
        while self.c1 is None or self.c2 is None:
            if self.is_host:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((self.ip,self.port))
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.listen(2)

                c, addr = s.accept()
                secret_message = TwoWayConnection.secret_message()
                c.send(secret_message)

                print(b'sent' + secret_message)
                annodda_c, addr = s.accept()
                message = annodda_c.recv(1024)

                

                print(b'received' + message)
                if message != secret_message:
                    c.close()
                    annodda_c.close()
                    s.close()
                    c.send(b'nope')
                    print('closed')
                    continue
                else:
                    self.c1 = annodda_c
                    self.c2 = c
                    self.s = s
                    c.send(b'ready')
                    break
            else:
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.ip,self.port))
                message = s.recv(1024)
                
                print(b'recieved ' + message)
                annodda_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                annodda_c.connect((self.ip,self.port))
                annodda_c.send(message)

                message = s.recv(1024)
                if message == b'nope':
                    s.close()
                    annodda_c.close()
                    print('closed')
                else:
                    print('accepted')
                    self.c1 = annodda_c
                    self.c2 = s
                    break
        self.outbox_thread.start()
        self.inbox_thread.start()
                

                
                
    def send_message(self,message):
        print(( b'host ' if self.is_host else b'client ')+ str(message).encode())
        
        self.outbox.put(message)
    def send_messages(self):
        while not self.should_end:
            item = self.outbox.get()
            self.c1.send(item.to_bytes() if type(item) is not bytes else item)
            print(item)
            print('sent')
            if item == b'q':
                self.should_end = True
            

    def receive_messages(self):
        while not self.should_end:
            if self.c2 is not None:
                message = self.c1.recv(1024)
                self.inbox.put(message)
                print(message)
                print('recieved')
                if message == b'' or message == b'q':
                    should_end = True

    def close(self):
        self.c1.close()
        self.c2.close()
        if self.s is not None:
            self.s.close()
    

windowsize = 750

init_window(windowsize, windowsize, b"TicTacToe")
set_target_fps(60)


squares = None
turn = None
player = None


# Define a variable to keep track of whether the game is over and who the winner is
game_over = False
winner = None
winning_combination = []


def game_init():
    global squares
    global turn
    global game_over
    global winner
    global winning_combination
    squares = [[Square.EMPTY, Square.EMPTY, Square.EMPTY],
               [Square.EMPTY, Square.EMPTY, Square.EMPTY],
               [Square.EMPTY, Square.EMPTY, Square.EMPTY]]
    turn = [Square.X, Square.O][random.randint(0, 1)]
    
    game_over = False
    winner = None
    winning_combination = []


class Game_Mode:
    MAIN_MENU = 0
    LOCAL_MULTIPLAYER = 1
    ONLINE_MULTIPLAYER = 2
    AGAINST_AI = 3
    HOST_OR_CLIENT_MENU = 4

game_mode = Game_Mode.MAIN_MENU



obamagreen = Color()
obamagreen.r = 240
obamagreen.g = 248
obamagreen.b = 215
obamagreen.a = 255

def main_menu():
    global game_mode
    def game_mode_selection():
        global player
        global turn
        mp = get_mouse_position()
        if mp.x > 150 and mp.y > 150 and mp.x < 4*150 and mp.y < 2*150:
            game_init()
            player = turn
            return Game_Mode.LOCAL_MULTIPLAYER
        elif mp.x > 150 and mp.y > 150 * 3 and mp.x < 4*150 and mp.y < 4*150:
            return Game_Mode.HOST_OR_CLIENT_MENU
        else:
            return None
                
    draw_text(b"Welcome to EPIC TIC TAC TOE (name subject to change)", 150, 50, 20, WHITE)

    draw_rectangle(150, 150, 150*3, 150, WHITE)
    draw_text(b"Local Multiplayer", 150, 150, 50, ORANGE)

    draw_rectangle(150, 3*150, 150*3, 150, WHITE)            
    draw_text(b"Online Multiplayer", 150, 3*150, 50, ORANGE)

    if is_mouse_button_down(0) and game_mode_selection() is not None:
        game_mode = game_mode_selection()





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
            if squares[i][j] == Square.EMPTY:
                pass
            elif squares[i][j] == Square.O:
                draw_circle(225+150*j, 225+150*i, 75, WHITE)
            else:
                draw_line_ex(Vector2(150+150*j, 150+150*i), Vector2(150*2+150*j, 150*2+150*i), 3, ORANGE)
                draw_line_ex(Vector2(150*2+150*j, 150+150*i), Vector2(150+150*j, 150*2+150*i), 3, ORANGE)

# Define the draw_top_text function to display the player's turn
def draw_top_text(text):
    draw_text(text, 50, 50, 20, obamagreen)
def draw_secondary_top_text(text):
    draw_text(text, 50, 100, 20, obamagreen)


    
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
    turn = Square.X if turn == Square.O else Square.O


# Define the find_winning_combination function to check for a win
def find_winning_combination():
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


def toggle_player():
    global player
    player = Square.X if player == Square.O else Square.O

def game_logic():
    global game_mode
    global game_over
    global winner
    global winning_combination
    global player
    global connection
    global squares
    draw_top_text(b'Player '+ (b'X' if turn == Square.X else b'O')+ b'\'s turn.')
    if game_mode != Game_Mode.LOCAL_MULTIPLAYER:
        draw_text(b'You are player ' + (b'O' if player == Square.O else b'X'), 150, 100, 40, WHITE)
    draw_board()
    draw_squares()
    if turn == player:
        # Check for mouse
        if is_mouse_button_pressed(0):
            row, col = get_mouse_square()
            if row is not None and col is not None and squares[row][col] == Square.EMPTY:
                squares[row][col] = player
                toggle_turn()
                if game_mode == Game_Mode.LOCAL_MULTIPLAYER:
                    toggle_player()
                elif game_mode == Game_Mode.ONLINE_MULTIPLAYER:
                    connection.send_message(row * 3 + col)
    else: # if turn != player
        if game_mode == Game_Mode.ONLINE_MULTIPLAYER:
            if not connection.inbox.empty():
                move = int.from_bytes(connection.inbox.get())
                squares[move // 3][move % 3] = Square.X if player == Square.O else Square.O
                toggle_turn()
        else: #if playing against AI
            move = make_AI_move()
            squares[move // 3][move % 3] = Square.X if player == Square.O else Square.O
            toggle_turn()

    winning_combination = find_winning_combination()
    if winning_combination:
        game_over = True
        winner = "X" if turn == Square.O else "O"
    elif all(squares[i][j] != Square.EMPTY for i in range(3) for j in range(3)):
        game_over = True
        winner = "Tie"

def make_AI_move():
    return None

other_accepted = False
you_accepted = False
other_quit = False
def game_over_screen():
    global squares
    global turn
    global winner
    global game_over
    global winning_combination
    global connection
    global player
    global game_mode
    global connection_started
    global other_accepted
    global you_accepted
    global other_quit
    draw_squares()
    draw_board()
    if winning_combination:
        for row, col in winning_combination:
            draw_circle(225 + 150 * col, 225 + 150 * row, 20, RED)
                
    # Display the winner or tie and the option to play again
    if winner == "Tie":
        draw_top_text("It's a tie! Press " + str(KEY_R) + " to play again.")
    else:
        if game_mode != Game_Mode.LOCAL_MULTIPLAYER:
            if not other_quit:
                if winner == "X" and player == Square.X or winner == "O" and player == Square.O:
                    draw_top_text("You Win. Press " + str(KEY_R) + " to play again.")
                else:
                    draw_top_text("You Lose. Press " + str(KEY_R) + " to play again.")
            else:
                if winner == "X" and player == Square.X or winner == "O" and player == Square.O:
                    draw_top_text("You Win. Other Player Quit.")
                else:
                    draw_top_text("You Lose. Other Player Quit.")
        else:
            draw_top_text("Winner is Player " + winner + ". Press " + str(KEY_R) + " to play again.")
            
    if game_mode == Game_Mode.ONLINE_MULTIPLAYER:

        if other_accepted and you_accepted and not other_quit:
            if connection.is_host:
                other_accepted = False
                you_accepted = False
                other_quit = False
                game_init()
                connection.send_message(("You are player " + ("O" if turn == Square.X else "X")).encode())
                player = turn
                game_mode = Game_Mode.ONLINE_MULTIPLAYER
            else:
                if not connection.inbox.empty():
                    response = connection.inbox.get()
                    if len(response) > 4:
                        other_accepted = False
                        you_accepted = False
                        other_quit = False
                        game_init()
                        player = Square.X if response[15] == 88 else Square.O
                        print(response[15])
                        turn = Square.O if player == Square.X else Square.X
                        game_mode = Game_Mode.ONLINE_MULTIPLAYER
        else:
            if not connection.inbox.empty():
                message = connection.inbox.get()
                if message == b'r':
                    other_accepted = True
                elif message == b'q':
                    other_quit = True

        if other_accepted and not other_quit:
            draw_secondary_top_text("Press " + str(KEY_Q) + " to Quit, but other player wants rematch.")
        elif you_accepted and not other_quit:
            draw_secondary_top_text("Sent rematch, request. Press " + str(KEY_Q) + " to Quit.")
        else:
            draw_secondary_top_text("Press " + str(KEY_Q) + " to Quit.")
    else:
        draw_secondary_top_text("Press " + str(KEY_Q) + " to Quit.")


    
        
    
        # Check for rematch option (pressing the 'R' key)
    if not other_quit and is_key_pressed(KEY_R):
        # Reset the game state for a rematch
        if game_mode == Game_Mode.ONLINE_MULTIPLAYER:
            connection.send_message(b'r')
            you_accepted = True
        else:
            game_init()
            if game_mode == Game_Mode.LOCAL_MULTIPLAYER:
                player = turn
            game_over = False
    if is_key_pressed(KEY_Q):
        game_init()
        other_quit = False
        other_accepted = False
        you_accepted = False
        if connection is not None:
            connection.send_message(b'q')
            connection.outbox_thread.join()
            connection.close()
        connection = None
        connection_started = False
        join_code = b''
        game_mode = Game_Mode.MAIN_MENU
        

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

connection = None

game_started = False


connection_started = False
def host_mode():
    global join_code
    global turn
    global player
    global game_started
    global connection
    global connection_started
    global game_mode
    if connection == None or connection.c1 is None or connection.c2 is None:
        if turn == Square.X:
            draw_text(b"You are player X", 150, 150, 30, ORANGE)
        else:
            draw_text(b"You are player O", 150, 150, 30, ORANGE)
    
        join_code = generate_join_code()
        draw_text(b"Your join code is " + join_code, 150, 3*150, 30, ORANGE)
        if connection == None:
            connection = TwoWayConnection(join_code,12345,True)
    elif not connection_started:
        connection.send_message(("You are player " + ("O" if turn == Square.X else "X")).encode())
        player = turn
        connection_started = True
    else:
        game_mode = Game_Mode.ONLINE_MULTIPLAYER

        
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
    global game_mode
    global join_code
    global player
    global turn
    global connection
    global connection_started
    if not connection_started:
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
                connection_started = True
                IP = join_code.decode()
                print("CONNECTING" + IP)
                connection = TwoWayConnection(IP,12345,False)
    elif not connection.inbox.empty():
        response = connection.inbox.get()
        print(response)
        
        player = Square.X if response[15] == 88 else Square.O
        print(response[15])
        turn = Square.O if player == Square.X else Square.X
        game_mode = Game_Mode.ONLINE_MULTIPLAYER
    else:
        print('waiting')
host_or_client = None

class HostOrClient:
    HOST = 0
    CLIENT = 1

def host_or_client_menu():
    def ask_to_be_host_or_client():
        global host_or_client
        def mode_selection():
            mp = get_mouse_position()
            if mp.x > 150 and mp.y > 150 and mp.x < 4*150 and mp.y < 2*150:
                return HostOrClient.HOST
            elif mp.x > 150 and mp.y > 150 * 3 and mp.x < 4*150 and mp.y < 4*150:
                return HostOrClient.CLIENT
            else:
                return None
            
        draw_text(b"Do you want to be the host or client?", 150, 50, 20, WHITE)

        draw_rectangle(150, 150, 150*3, 150, WHITE)
        draw_text(b"Host", 150, 150, 50, ORANGE)

        draw_rectangle(150, 3*150, 150*3, 150, WHITE)            
        draw_text(b"Client", 150, 3*150, 50, ORANGE)
        if is_mouse_button_pressed(0) and mode_selection() is not None:
            host_or_client = mode_selection()
            game_init()
        
    if host_or_client is None:
        ask_to_be_host_or_client()
    elif host_or_client == HostOrClient.HOST:
        host_mode()
    else:
        game_init()
        client_mode()
    
# Main game loop
while not window_should_close():
    begin_drawing()
    clear_background(Color(48, 213, 200, 255))

    if game_mode == Game_Mode.MAIN_MENU:
        main_menu()
    elif game_mode == Game_Mode.HOST_OR_CLIENT_MENU:
        host_or_client_menu()
    elif not game_over:
        game_logic()
    else:
        game_over_screen()


    
    end_drawing()

# Close the game window
close_window()



    


#a thing that gets the mouse position and changes a square (DONE)
#a turn tracker (DONE)
#something to check if someone one (DONE)
#game over screen (DONE)
#text on top (DONE)
#the stuff on the bottom
#local multiplayer
#online multiplayer
#against CPU
#leaderboard
#ADS TO MAKE MONEY
#NFT
#SWIFT??
