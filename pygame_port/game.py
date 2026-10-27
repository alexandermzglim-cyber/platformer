"""Settings and menu choices shared by the whole game."""

# The game was designed for a 3200 x 1500 pixel screen. All positions in the
# menus use these "game pixels". render.py shrinks everything to fit your monitor.
GAME_WIDTH: int = 3200
GAME_HEIGHT: int = 1500

LEVEL_COUNT: int = 3

# The words shown in each menu. The player's choice is stored as a position in
# one of these lists, e.g. 0 means the first item.
MAIN_MENU_OPTIONS: list[str] = ["PLAY", "EDITOR", "QUIT"]
PAUSE_MENU_OPTIONS: list[str] = ["RESUME", "LEVEL_SELECT", "MAIN MENU", "QUIT"]


class Game:
    """Remembers which screen we're on and what is highlighted in each menu."""

    def __init__(self) -> None:
        # Which screen is showing. It is always one of these words:
        #   "menu", "level_select", "playing", "paused", "level_complete", "editor"
        self.state: str = "menu"

        # Set to False to close the game.
        self.running: bool = True

        # Which item is highlighted in each menu (0 = the first item).
        self.main_menu_selected: int = 0
        self.level_selected: int = 0
        self.pause_menu_selected: int = 0

        # Set to True when the player presses Enter on the level select screen.
        # main.py sees it, loads the level, then sets it back to False.
        self.start_level_requested: bool = False

        # One True/False per level, recording which levels have been finished.
        self.levels_completed: list[bool] = [False] * LEVEL_COUNT


def move_selection(selected: int, change: int, option_count: int) -> int:
    """Move a menu highlight up (change = -1) or down (change = +1), wrapping around the ends."""
    selected = selected + change
    if selected < 0:
        selected = option_count - 1
    if selected >= option_count:
        selected = 0
    return selected
