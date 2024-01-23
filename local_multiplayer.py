from shared import *
import shared_vars


class Move:
    def __init__(self,player,position):
        self.player = player
        self.position = position

class Local_Multiplayer_Game:
    def __init__(self):
        self.squares = [[Square.EMPTY,Square.EMPTY,Square.EMPTY],
                      [Square.EMPTY,Square.EMPTY,Square.EMPTY],
                      [Square.EMPTY,Square.EMPTY,Square.EMPTY]]
        self.turn = Player.X # X always goes first
        self.human_players_here = [Player.X,Player.O] #Both Players are playing at this computer
        self.turn_history = [] #to calculate turn
        self.rematch_accepted = False
        self.rematch_requested = False
        self.other_quit = False
        self.game_quit = False

    def do_move(self,player,move):
        self.turn_history.append(Move(player,move))
        self.squares[(move - 1)//3][(move - 1)% 3] = player

    def request_rematch(self):
        self.rematch_requested = True
        self.rematch_accepted = True

    def see_whos_turn_it_is(self):
        if len(self.turn_history) == 0:
            return Player.X
        elif self.turn_history[-1].player == Player.X:
            return Player.O
        else:
            return Player.X

    def get_squares(self):
        return self.squares
        
    def is_waiting(self):
        return False

    def quit_game(self):
        self.game_quit = True

def local_multiplayer_view():

    if not shared_vars.game:
        shared_vars.game = Local_Multiplayer_Game()
    game_over = game_logic(shared_vars.game)
    if game_over:
        game_over_screen(shared_vars.game)
        if shared_vars.game.rematch_accepted:
            shared_vars.game = Local_Multiplayer_Game()
        elif shared_vars.game.game_quit:

            shared_vars.view = shared_vars.main_menu
            shared_vars.game = None

