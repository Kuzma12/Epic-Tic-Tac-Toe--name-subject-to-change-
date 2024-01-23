from shared import *
import shared_vars
from local_multiplayer import *
from online_multiplayer import *





def main_menu_view():
    
    draw_text(b"Welcome to EPIC TIC TAC TOE (name subject to change)", 150, 50, 20, WHITE)

    draw_rectangle(150, 150, 150*3, 150, WHITE)
    draw_text(b"Local Multiplayer", 150, 150, 50, ORANGE)
    
    draw_rectangle(150, 3*150, 150*3, 150, WHITE)            
    draw_text(b"Online Multiplayer", 150, 3*150, 50, ORANGE)

    game_mode_selection = None
    if is_mouse_button_down(0):
        mp = get_mouse_position()
    
        if mp.x > 150 and mp.y > 150 and mp.x < 4*150 and mp.y < 2*150:
            game_mode_selection = local_multiplayer_view
        elif mp.x > 150 and mp.y > 150 * 3 and mp.x < 4*150 and mp.y < 4*150:
            game_mode_selection = online_multiplayer_view
        if game_mode_selection:
            shared_vars.view = game_mode_selection

init_window(shared_vars.windowsize,
            shared_vars.windowsize,
            b"EPIC TIC TAC TOE (name subject to change)")
set_target_fps(60)

shared_vars.view = main_menu_view
shared_vars.main_menu = main_menu_view


while not window_should_close():
    begin_drawing()
    clear_background(Color(48, 213, 200, 255))
    shared_vars.view()
    end_drawing()

