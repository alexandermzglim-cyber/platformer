import time

import pygame

from camera import Camera
from game import Game, State
from input_handler import handle_key_event, update_held_keys
from level import Level
from player import Player
from render import Renderer

LOGICAL_W = 3200
LOGICAL_H = 1500
MAX_DT = 0.05
CAMERA_ZOOM = 2.5
SPAWN_POSITION = (10.0, 5.0)
SCREEN_FILL_FRACTION = 0.9


def create_window():
    desktop_w, desktop_h = pygame.display.get_desktop_sizes()[0]
    fit = min(desktop_w * SCREEN_FILL_FRACTION / LOGICAL_W,
              desktop_h * SCREEN_FILL_FRACTION / LOGICAL_H, 1.0)
    window = pygame.display.set_mode((round(LOGICAL_W * fit), round(LOGICAL_H * fit)), pygame.RESIZABLE)
    pygame.display.set_caption("Platformer Game")
    return window


def main():
    pygame.init()
    window = create_window()
    renderer = Renderer(window, LOGICAL_W, LOGICAL_H)
    clock = pygame.time.Clock()

    game = Game()
    camera = Camera(CAMERA_ZOOM, LOGICAL_W, LOGICAL_H)
    player = Player(400.0, 300.0)
    level = None

    last_time = time.perf_counter()
    first_frame = True
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.VIDEORESIZE:
                renderer.update_viewport()
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                handle_key_event(game, player, event)
        if not game.running:
            break

        current_time = time.perf_counter()
        dt = current_time - last_time
        if not first_frame and not pygame.key.get_focused():
            last_time = current_time
            clock.tick(30)
            continue
        first_frame = False
        dt = min(dt, MAX_DT)
        last_time = current_time

        if game.state == State.MENU:
            renderer.draw_menu(game)
        elif game.state == State.LEVEL_SELECT:
            renderer.draw_level_select(game)
            if game.level_confirmation:
                level = Level(game.level_selected)
                player.reset(*SPAWN_POSITION)
                game.level_confirmation = False
                game.state = State.PLAYING
        elif game.state == State.PLAYING:
            update_held_keys(game, player, dt)
            player.update(level, dt)
            if player.on_goal(level):
                game.level_completed = True
            if player.on_spike(level) or player.fell_off_level(level):
                player.reset(*SPAWN_POSITION)
            if game.level_completed:
                game.level_completed = False
                game.levels_completed[game.level_selected] = True
                game.state = State.LEVEL_COMPLETE
            camera.update(player, LOGICAL_W, LOGICAL_H, dt)
            renderer.draw_world(level, player, camera)
        elif game.state == State.PAUSED:
            renderer.draw_pause(game)
        elif game.state == State.LEVEL_COMPLETE:
            renderer.draw_level_complete()
        elif game.state == State.EDITOR:
            renderer.draw_editor()

        pygame.display.flip()
        clock.tick(240)

    pygame.quit()


if __name__ == "__main__":
    main()
