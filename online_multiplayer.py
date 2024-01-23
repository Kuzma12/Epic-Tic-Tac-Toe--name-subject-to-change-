from shared import *
import shared_vars
import requests
import re
import time

class Online_Multiplayer_Game():

    website_name = "http://localhost:8000"
    def __init__(self, game_number=None, passcode=None):
        self.squares = [[Square.EMPTY, Square.EMPTY, Square.EMPTY],
                        [Square.EMPTY, Square.EMPTY, Square.EMPTY],
                        [Square.EMPTY, Square.EMPTY, Square.EMPTY]]
        error = None
        if not game_number or not passcode:
            self.game_number, self.passcode, error = Online_Multiplayer_Game.newgame()
        self.turn_history = []
        self.human_players_here = []
        self.rematch_requested = False
        self.rematch_accepted  = False
        self.game_quit = False
        self.other_quit = False
        if error:
            display_error(error)
            self.__init__()
        else:
             x_or_o, error= Online_Multiplayer_Game.am_i_x_or_o(self.game_number,self.passcode)
             if error:
                display_error(error)
                self.__init__()
             else:
                 self.human_players_here.append(x_or_o)

    def do_move(self,player,move):
        response = requests.get( Online_Multiplayer_Game.website_name+ "/move?game={game_number}&key={key}&move={move}".format(game_number = self.game_number, key = self.passcode,move = move))
        self.turn_history.append(Move(player,move))
        self.squares[(move - 1)//3][(move - 1)% 3] = player


    def see_whos_turn_it_is(self):
        if len(self.turn_history) == 0:
            return Player.X
        elif self.turn_history[-1].player == Player.X:
            return Player.O
        else:
            return Player.X

    def wait_for_other_player(self):
        time.sleep(0.1)
        response = requests.get(Online_Multiplayer_Game.website_name+ "/lastmove?game={game_number}&key={key}".format(game_number = self.game_number, key = self.passcode))
        new_move = Online_Multiplayer_Game.parse_move(response.text)
        print(response.text)
        if new_move:
            for move in self.turn_history:
                if move.position == new_move.position:
                    return
            print(new_move.player)
            self.turn_history.append(new_move)
            self.squares[(new_move.position - 1)//3][(new_move.position - 1)% 3] = new_move.player

    def quit_game(self):
        requests.get(Online_Multiplayer_Game.website_name+ "/move?game={game_number}&key={key}&move=q".format(game_number = self.game_number, key = self.passcode))
        self.game_quit = True



    def parse_move(text):
        if re.match(r"Player:[XO] Position:[0-9]", text):
            player = re.search(r"Player:[XO]", text).group()[7:8]
            move = re.search(r"Position:[0-9]", text).group()[9:11]
            return Move(Player.X if player == "X" or player == "x" else Player.O, int(move))
        else:
            if re.match(r"Player:[XO] Position:[0-9]", text):
                self.game_quit = True
            return None
        

    def newgame():
        response = requests.get(Online_Multiplayer_Game.website_name + "/newgame")
        if response:
            if re.match(r"Game Number:[0-9]* Passcode:[0-9]*", response.text):
                game_number = re.search(r"Game Number:[0-9]*", response.text).group()[12:]
                
                passcode = re.search(r"Passcode:[0-9]*", response.text).group()[9:]
                error = None
                return game_number, passcode, error
            elif re.match(r"Error:", response.text):
                return None, None, response.text
            else:
                return None, None, "Error: Something's wrong with the website"
        else:
            return None, None, "Error: Something's wrong with the website"

    def am_i_x_or_o(game_number, key):
        response = requests.get(Online_Multiplayer_Game.website_name + "/am-i-x-or-o?game={game_number}&key={key}".format(game_number = game_number, key = key))
        if response:
            if re.match(r"You are [XO].", response.text):
                x_or_o = re.search(r"You are [XO].", response.text).group()[8:9]
                error = None
                return Player.X if x_or_o == "X" else Player.O, error
            elif re.match(r"Error:", response.text):
                return None,response.text
            else:
                return None, "Error: Something's wrong with the website"
        else:
            return None, "Error: Something's wrong with the website"
    
def online_multiplayer_view():
    if not shared_vars.game:
        shared_vars.game = Online_Multiplayer_Game()
    game_over = game_logic(shared_vars.game)
    if game_over:
        game_over_screen(shared_vars.game)
        if shared_vars.game.rematch_accepted:
            shared_vars.game = Online_Multiplayer_Game()
        elif shared_vars.game.game_quit:
            shared_vars.view = shared_vars.main_menu
            shared_vars.game = None
