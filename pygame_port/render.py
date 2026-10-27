"""Everything that draws to the screen.

All positions here are in "game pixels" on a 3200 x 1500 screen. Most monitors
are smaller than that, so the Renderer works out one number, `scale`, and
multiplies every position and size by it before drawing.
"""

from pathlib import Path

import pygame

from camera import Camera
from game import Game, GAME_WIDTH, GAME_HEIGHT, MAIN_MENU_OPTIONS, PAUSE_MENU_OPTIONS, LEVEL_COUNT
from level import Level, PROJECT_FOLDER, BLOCK, SPIKE, GOAL, TILE_SIZE
from player import Player, PLAYER_WIDTH, PLAYER_HEIGHT

# A colour is three whole numbers: (red, green, blue), each from 0 to 255.
# Giving this type a name makes the hints below easier to read.
Colour = tuple[int, int, int]

# A point is an (x, y) pair of positions.
Point = tuple[float, float]

WHITE: Colour = (255, 255, 255)
BLACK: Colour = (0, 0, 0)
GREY: Colour = (153, 153, 153)
RED: Colour = (255, 0, 0)
GREEN: Colour = (0, 255, 0)

FONT_FILE: Path = PROJECT_FOLDER / "font" / "ttf" / "JetBrainsMono-Regular.ttf"
TITLE_FONT_SIZE: int = 97   # font sizes in game pixels, before scaling
ITEM_FONT_SIZE: int = 87

# Where the menus go, in game pixels from the top-left corner.
MENU_X: int = 1450          # centre of the menu text
ARROW_X: int = 1210         # centre of the "->" arrow
PAUSE_ARROW_X: int = 1100
TITLE_Y: int = 850
FIRST_ITEM_Y: int = 1000
ITEM_SPACING: int = 150     # gap between menu lines

# Leave a little room around the window so it fits on screen with the taskbar.
SCREEN_FILL: float = 0.9


class Renderer:
    def __init__(self) -> None:
        monitor_width, monitor_height = pygame.display.get_desktop_sizes()[0]

        # Pick the largest scale that still fits on this monitor, but never bigger than 1.
        self.scale: float = min(monitor_width * SCREEN_FILL / GAME_WIDTH,
                                monitor_height * SCREEN_FILL / GAME_HEIGHT,
                                1.0)

        window_width: int = round(GAME_WIDTH * self.scale)
        window_height: int = round(GAME_HEIGHT * self.scale)
        # A Surface is pygame's word for a picture you can draw on. This one is the window.
        self.screen: pygame.Surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Platformer Game")

        self.title_font: pygame.font.Font = pygame.font.Font(FONT_FILE, round(TITLE_FONT_SIZE * self.scale))
        self.item_font: pygame.font.Font = pygame.font.Font(FONT_FILE, round(ITEM_FONT_SIZE * self.scale))

    # ---- Small drawing helpers ----

    def draw_text(self, text: str, x: float, y: float, font: pygame.font.Font, colour: Colour = BLACK) -> None:
        """Draw text with its centre at (x, y) game pixels."""
        image: pygame.Surface = font.render(text, True, colour)
        left: float = x * self.scale - image.get_width() / 2
        top: float = y * self.scale - image.get_height() / 2
        self.screen.blit(image, (left, top))

    def world_to_screen(self, camera: Camera, world_x: float, world_y: float) -> tuple[int, int]:
        """Turn a position in the level into a position in the window.

        First subtract the camera position (so things move as the camera moves),
        then multiply by zoom (to make the level bigger), then by scale (to fit your monitor).
        """
        screen_x: float = (world_x - camera.x) * camera.zoom * self.scale
        screen_y: float = (world_y - camera.y) * camera.zoom * self.scale
        return round(screen_x), round(screen_y)

    def draw_world_rectangle(self, camera: Camera, x: float, y: float,
                             width: float, height: float, colour: Colour) -> None:
        left, top = self.world_to_screen(camera, x, y)
        right, bottom = self.world_to_screen(camera, x + width, y + height)
        pygame.draw.rect(self.screen, colour, (left, top, right - left, bottom - top))

    def draw_world_triangle(self, camera: Camera, corner1: Point, corner2: Point,
                            corner3: Point, colour: Colour) -> None:
        points: list[tuple[int, int]] = [
            self.world_to_screen(camera, corner1[0], corner1[1]),
            self.world_to_screen(camera, corner2[0], corner2[1]),
            self.world_to_screen(camera, corner3[0], corner3[1]),
        ]
        pygame.draw.polygon(self.screen, colour, points)

    # ---- One function per screen ----

    def draw_main_menu(self, game: Game) -> None:
        self.screen.fill(WHITE)
        self.draw_text("PLATFORMER", MENU_X, TITLE_Y, self.title_font)
        for index in range(len(MAIN_MENU_OPTIONS)):
            y: int = FIRST_ITEM_Y + index * ITEM_SPACING
            self.draw_text(MAIN_MENU_OPTIONS[index], MENU_X, y, self.item_font)
            if index == game.main_menu_selected:
                self.draw_text("->", ARROW_X, y, self.item_font)

    def draw_level_select(self, game: Game) -> None:
        self.screen.fill(WHITE)
        self.draw_text("SELECT LEVEL", MENU_X, TITLE_Y, self.title_font)
        for index in range(LEVEL_COUNT):
            y: int = FIRST_ITEM_Y + index * ITEM_SPACING
            self.draw_text(f"LEVEL {index + 1}", MENU_X, y, self.item_font)
            if index == game.level_selected:
                self.draw_text("->", ARROW_X, y, self.item_font)

    def draw_pause_menu(self, game: Game) -> None:
        self.screen.fill(WHITE)
        for index in range(len(PAUSE_MENU_OPTIONS)):
            y: int = FIRST_ITEM_Y + index * ITEM_SPACING
            self.draw_text(PAUSE_MENU_OPTIONS[index], MENU_X, y, self.item_font)
            if index == game.pause_menu_selected:
                self.draw_text("->", PAUSE_ARROW_X, y, self.item_font)

    def draw_level_complete(self) -> None:
        self.screen.fill(WHITE)
        self.draw_text("LEVEL COMPLETED!", 1350, FIRST_ITEM_Y, self.item_font, GREEN)
        self.draw_text("PRESS_ENTER", 1350, FIRST_ITEM_Y + ITEM_SPACING, self.item_font)

    def draw_editor(self) -> None:
        self.screen.fill(WHITE)
        self.draw_text("EDITOR NOT AVAILABLE", MENU_X, TITLE_Y, self.item_font)
        self.draw_text("PRESS ESCAPE", MENU_X, FIRST_ITEM_Y, self.item_font)

    def draw_level(self, level: Level, player: Player, camera: Camera) -> None:
        self.screen.fill(WHITE)

        for row in range(level.height):
            for column in range(level.width):
                tile: int = level.tiles[row][column]
                x: int = column * TILE_SIZE
                y: int = row * TILE_SIZE

                if tile == BLOCK:
                    self.draw_world_rectangle(camera, x, y, TILE_SIZE, TILE_SIZE, GREY)
                elif tile == SPIKE:
                    bottom_left: Point = (x, y + TILE_SIZE)
                    bottom_right: Point = (x + TILE_SIZE, y + TILE_SIZE)
                    top_middle: Point = (x + TILE_SIZE // 2, y)
                    self.draw_world_triangle(camera, bottom_left, bottom_right, top_middle, RED)
                elif tile == GOAL:
                    self.draw_world_rectangle(camera, x, y, TILE_SIZE, TILE_SIZE, GREEN)

        self.draw_world_rectangle(camera, player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT, RED)
