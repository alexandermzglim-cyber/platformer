"""Settings and menu choices shared by the whole game."""

# The game was designed for a 3200 x 1500 pixel screen. All positions in the
# menus use these "game pixels". render.py shrinks everything to fit your monitor.
GAME_WIDTH = 3200
GAME_HEIGHT = 1500

LEVEL_COUNT = 3

# The words shown in each menu. The player's choice is stored as a position in
# one of these lists, e.g. 0 means the first item.
MAIN_MENU_OPTIONS = ["PLAY", "EDITOR", "QUIT"]
PAUSE_MENU_OPTIONS = ["RESUME", "LEVEL_SELECT", "MAIN MENU", "QUIT"]


class Game:
    """Remembers which screen we're on and what is highlighted in each menu."""

    def __init__(self):
        # Which screen is showing. It is always one of these words:
        #   "menu", "level_select", "playing", "paused", "level_complete", "editor"
        self.state = "menu"

        # Set to False to close the game.
        self.running = True

        # Which item is highlighted in each menu.
        self.main_menu_selected = 0
        self.level_selected = 0
        self.pause_menu_selected = 0

        # Set to True when the player presses Enter on the level select screen.
        # main.py sees it, loads the level, then sets it back to False.
        self.start_level_requested = False

        # One True/False per level, recording which levels have been finished.
        self.levels_completed = [False] * LEVEL_COUNT


def move_selection(selected, change, option_count):
    """Move a menu highlight up (change = -1) or down (change = +1), wrapping around the ends."""
    selected = selected + change
    if selected < 0:
        selected = option_count - 1
    if selected >= option_count:
        selected = 0
    return selected
