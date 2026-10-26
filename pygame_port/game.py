from enum import Enum, auto


class State(Enum):
    MENU = auto()
    PLAYING = auto()
    LEVEL_SELECT = auto()
    EDITOR = auto()
    PAUSED = auto()
    LEVEL_COMPLETE = auto()


MENU_PLAY = 0
MENU_EDITOR = 1
MENU_QUIT = 2
MENU_COUNT = 3

PAUSE_RESUME = 0
PAUSE_LEVEL_SELECT = 1
PAUSE_MAIN_MENU = 2
PAUSE_QUIT = 3
PAUSE_COUNT = 4


class Game:
    def __init__(self):
        self.state = State.MENU
        self.running = True
        self.main_menu_selected = 0
        self.level_selected = 0
        self.level_count = 3
        self.pause_selected = 0
        self.level_confirmation = False
        self.level_completed = False
        self.levels_completed = [False] * 100
