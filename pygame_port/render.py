import pygame

from level import PROJECT_ROOT, TILE_SOLID, TILE_SPIKE, TILE_GOAL
from player import TILE_SIZE, PLAYER_WIDTH, PLAYER_HEIGHT

FONT_PATH = PROJECT_ROOT / "font" / "ttf" / "JetBrainsMono-Regular.ttf"
FONT_PIXEL_HEIGHT = 128

BACKGROUND = (255, 255, 255)
BLOCK = (153, 153, 153)
SPIKE = (255, 0, 0)
GOAL = (0, 255, 0)
PLAYER = (255, 0, 0)
TEXT = (0, 0, 0)
TEXT_SUCCESS = (0, 255, 0)

MENU_X = 1450
ARROW_X = 1210
PAUSE_ARROW_X = 1100
TITLE_SCALE = 1.0
ITEM_SCALE = 0.9


class Renderer:
    """Draws in the game's 3200x1500 logical coordinates, scaled to fit the real window."""

    def __init__(self, window, logical_w, logical_h):
        self.window = window
        self.logical_w = logical_w
        self.logical_h = logical_h
        probe = pygame.font.Font(FONT_PATH, 100)
        self._font_size_per_pixel = 100 / (probe.get_ascent() - probe.get_descent())
        self._fonts = {}
        self.update_viewport()

    def update_viewport(self):
        window_w, window_h = self.window.get_size()
        self.view_scale = min(window_w / self.logical_w, window_h / self.logical_h)
        self.offset_x = (window_w - self.logical_w * self.view_scale) / 2
        self.offset_y = (window_h - self.logical_h * self.view_scale) / 2
        self._fonts.clear()

    def _to_window(self, x, y):
        return self.offset_x + x * self.view_scale, self.offset_y + y * self.view_scale

    def _clear(self):
        self.window.set_clip(None)
        self.window.fill(BACKGROUND)
        left, top = self._to_window(0, 0)
        self.window.set_clip(pygame.Rect(round(left), round(top),
                                         round(self.logical_w * self.view_scale),
                                         round(self.logical_h * self.view_scale)))

    def _font(self, scale):
        pixel_height = FONT_PIXEL_HEIGHT * scale * self.view_scale
        size = max(1, round(pixel_height * self._font_size_per_pixel))
        if size not in self._fonts:
            self._fonts[size] = pygame.font.Font(FONT_PATH, size)
        return self._fonts[size]

    def _text(self, text, x, y, scale, color=TEXT, anchor_x=0.5, anchor_y=0.5):
        """y is measured up from the bottom of the screen, as in the original OpenGL code."""
        font = self._font(scale)
        surface = font.render(text, True, color)
        text_height = font.get_ascent() - font.get_descent()
        window_x, window_y = self._to_window(x, self.logical_h - y)
        self.window.blit(surface, (round(window_x - surface.get_width() * anchor_x),
                                   round(window_y - text_height * anchor_y)))

    def _world_rect(self, camera, x, y, w, h, color):
        left, top = self._world_to_window(camera, x, y)
        right, bottom = self._world_to_window(camera, x + w, y + h)
        pygame.draw.rect(self.window, color, pygame.Rect(left, top, right - left, bottom - top))

    def _world_triangle(self, camera, points, color):
        pygame.draw.polygon(self.window, color, [self._world_to_window(camera, x, y) for x, y in points])

    def _world_to_window(self, camera, x, y):
        window_x, window_y = self._to_window((x - camera.x) * camera.zoom, (y - camera.y) * camera.zoom)
        return round(window_x), round(window_y)

    def draw_menu(self, game):
        self._clear()
        self._text("PLATFORMER", MENU_X, 650, TITLE_SCALE)
        items = ["PLAY", "EDITOR", "QUIT"]
        for index, (label, y) in enumerate(zip(items, (500, 350, 200))):
            self._text(label, MENU_X, y, ITEM_SCALE)
            if index == game.main_menu_selected:
                self._text("->", ARROW_X, y, ITEM_SCALE)

    def draw_level_select(self, game):
        self._clear()
        self._text("SELECT LEVEL", MENU_X, 650, TITLE_SCALE)
        y = 500
        for index in range(game.level_count):
            self._text(f"LEVEL {index + 1}", MENU_X, y, ITEM_SCALE)
            if index == game.level_selected:
                self._text("->", ARROW_X, y, ITEM_SCALE)
            y -= 150

    def draw_pause(self, game):
        self._clear()
        items = [("RESUME", 1450, 500), ("LEVEL_SELECT", 1459, 350), ("MAIN MENU", 1450, 200), ("QUIT", 1450, 50)]
        for index, (label, x, y) in enumerate(items):
            self._text(label, x, y, ITEM_SCALE)
            if index == game.pause_selected:
                self._text("->", PAUSE_ARROW_X, y, ITEM_SCALE)

    def draw_level_complete(self):
        self._clear()
        self._text("LEVEL COMPLETED!", 1350, 500, ITEM_SCALE, TEXT_SUCCESS)
        self._text("PRESS_ENTER", 1350, 350, ITEM_SCALE)

    def draw_editor(self):
        self._clear()
        self._text("EDITOR NOT AVAILABLE", MENU_X, 650, ITEM_SCALE)
        self._text("PRESS ESCAPE", MENU_X, 500, ITEM_SCALE)

    def draw_world(self, level, player, camera):
        self._clear()
        first_x = int(camera.x / TILE_SIZE) - 1
        last_x = int((camera.x + self.logical_w / camera.zoom) / TILE_SIZE) + 1
        for tile_y in range(level.height):
            for tile_x in range(max(first_x, 0), min(last_x, level.width)):
                tile = level.tiles[tile_y][tile_x]
                world_x = tile_x * TILE_SIZE
                world_y = tile_y * TILE_SIZE
                if tile == TILE_SOLID:
                    self._world_rect(camera, world_x, world_y, TILE_SIZE, TILE_SIZE, BLOCK)
                elif tile == TILE_SPIKE:
                    self._world_triangle(camera, [
                        (world_x, world_y + TILE_SIZE),
                        (world_x + TILE_SIZE, world_y + TILE_SIZE),
                        (world_x + TILE_SIZE // 2, world_y),
                    ], SPIKE)
                elif tile == TILE_GOAL:
                    self._world_rect(camera, world_x, world_y, TILE_SIZE, TILE_SIZE, GOAL)
        self._world_rect(camera, player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER)
