"""Everything that draws to the screen.

All positions here are in "game pixels" on a 3200 x 1500 screen. Most monitors
are smaller than that, so the Renderer works out one number, `scale`, and
multiplies every position and size by it before drawing.
"""

import pygame

from game import GAME_WIDTH, GAME_HEIGHT, MAIN_MENU_OPTIONS, PAUSE_MENU_OPTIONS, LEVEL_COUNT
from level import PROJECT_FOLDER, BLOCK, SPIKE, GOAL, TILE_SIZE
from player import PLAYER_WIDTH, PLAYER_HEIGHT

# Colours are (red, green, blue), each from 0 to 255.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (153, 153, 153)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FONT_FILE = PROJECT_FOLDER / "font" / "ttf" / "JetBrainsMono-Regular.ttf"
TITLE_FONT_SIZE = 97   # font sizes in game pixels, before scaling
ITEM_FONT_SIZE = 87

# Where the menus go, in game pixels from the top-left corner.
MENU_X = 1450          # centre of the menu text
ARROW_X = 1210         # centre of the "->" arrow
PAUSE_ARROW_X = 1100
TITLE_Y = 850
FIRST_ITEM_Y = 1000
ITEM_SPACING = 150     # gap between menu lines

# Leave a little room around the window so it fits on screen with the taskbar.
SCREEN_FILL = 0.9


class Renderer:
    def __init__(self):
        monitor_width, monitor_height = pygame.display.get_desktop_sizes()[0]

        # Pick the largest scale that still fits on this monitor, but never bigger than 1.
        self.scale = min(monitor_width * SCREEN_FILL / GAME_WIDTH,
                         monitor_height * SCREEN_FILL / GAME_HEIGHT,
                         1.0)

        window_width = round(GAME_WIDTH * self.scale)
        window_height = round(GAME_HEIGHT * self.scale)
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Platformer Game")

        self.title_font = pygame.font.Font(FONT_FILE, round(TITLE_FONT_SIZE * self.scale))
        self.item_font = pygame.font.Font(FONT_FILE, round(ITEM_FONT_SIZE * self.scale))

    # ---- Small drawing helpers ----

    def draw_text(self, text, x, y, font, colour=BLACK):
        """Draw text with its centre at (x, y) game pixels."""
        image = font.render(text, True, colour)
        left = x * self.scale - image.get_width() / 2
        top = y * self.scale - image.get_height() / 2
        self.screen.blit(image, (left, top))

    def world_to_screen(self, camera, world_x, world_y):
        """Turn a position in the level into a position in the window.

        First subtract the camera position (so things move as the camera moves),
        then multiply by zoom (to make the level bigger), then by scale (to fit your monitor).
        """
        screen_x = (world_x - camera.x) * camera.zoom * self.scale
        screen_y = (world_y - camera.y) * camera.zoom * self.scale
        return round(screen_x), round(screen_y)

    def draw_world_rectangle(self, camera, x, y, width, height, colour):
        left, top = self.world_to_screen(camera, x, y)
        right, bottom = self.world_to_screen(camera, x + width, y + height)
        pygame.draw.rect(self.screen, colour, (left, top, right - left, bottom - top))

    def draw_world_triangle(self, camera, corner1, corner2, corner3, colour):
        points = [
            self.world_to_screen(camera, corner1[0], corner1[1]),
            self.world_to_screen(camera, corner2[0], corner2[1]),
            self.world_to_screen(camera, corner3[0], corner3[1]),
        ]
        pygame.draw.polygon(self.screen, colour, points)

    # ---- One function per screen ----

    def draw_main_menu(self, game):
        self.screen.fill(WHITE)
        self.draw_text("PLATFORMER", MENU_X, TITLE_Y, self.title_font)
        for index in range(len(MAIN_MENU_OPTIONS)):
            y = FIRST_ITEM_Y + index * ITEM_SPACING
            self.draw_text(MAIN_MENU_OPTIONS[index], MENU_X, y, self.item_font)
            if index == game.main_menu_selected:
                self.draw_text("->", ARROW_X, y, self.item_font)

    def draw_level_select(self, game):
        self.screen.fill(WHITE)
        self.draw_text("SELECT LEVEL", MENU_X, TITLE_Y, self.title_font)
        for index in range(LEVEL_COUNT):
            y = FIRST_ITEM_Y + index * ITEM_SPACING
            self.draw_text(f"LEVEL {index + 1}", MENU_X, y, self.item_font)
            if index == game.level_selected:
                self.draw_text("->", ARROW_X, y, self.item_font)

    def draw_pause_menu(self, game):
        self.screen.fill(WHITE)
        for index in range(len(PAUSE_MENU_OPTIONS)):
            y = FIRST_ITEM_Y + index * ITEM_SPACING
            self.draw_text(PAUSE_MENU_OPTIONS[index], MENU_X, y, self.item_font)
            if index == game.pause_menu_selected:
                self.draw_text("->", PAUSE_ARROW_X, y, self.item_font)

    def draw_level_complete(self):
        self.screen.fill(WHITE)
        self.draw_text("LEVEL COMPLETED!", 1350, FIRST_ITEM_Y, self.item_font, GREEN)
        self.draw_text("PRESS_ENTER", 1350, FIRST_ITEM_Y + ITEM_SPACING, self.item_font)

    def draw_editor(self):
        self.screen.fill(WHITE)
        self.draw_text("EDITOR NOT AVAILABLE", MENU_X, TITLE_Y, self.item_font)
        self.draw_text("PRESS ESCAPE", MENU_X, FIRST_ITEM_Y, self.item_font)

    def draw_level(self, level, player, camera):
        self.screen.fill(WHITE)

        for row in range(level.height):
            for column in range(level.width):
                tile = level.tiles[row][column]
                x = column * TILE_SIZE
                y = row * TILE_SIZE

                if tile == BLOCK:
                    self.draw_world_rectangle(camera, x, y, TILE_SIZE, TILE_SIZE, GREY)
                elif tile == SPIKE:
                    bottom_left = (x, y + TILE_SIZE)
                    bottom_right = (x + TILE_SIZE, y + TILE_SIZE)
                    top_middle = (x + TILE_SIZE // 2, y)
                    self.draw_world_triangle(camera, bottom_left, bottom_right, top_middle, RED)
                elif tile == GOAL:
                    self.draw_world_rectangle(camera, x, y, TILE_SIZE, TILE_SIZE, GREEN)

        self.draw_world_rectangle(camera, player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT, RED)
