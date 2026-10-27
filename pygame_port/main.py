"""START HERE!  Run the game by typing this in a terminal:   python pygame_port/main.py

Every video game has a "game loop". It is a while loop that goes round and
round very fast (hundreds of times a second). Each time round it does 4 things:
  1. Check which keys are being pressed
  2. Work out how much time has passed
  3. Move everything and draw the picture
  4. Show the picture on the screen
Each picture is called a "frame".

The other files each look after one part of the game:
  game.py           - which screen we're on (menu, playing, paused...)
  level.py          - loads the levels from the .map files
  player.py         - how the red square moves and jumps
  camera.py         - which part of the level you can see
  input_handler.py  - what each key does
  render.py         - drawing everything

ABOUT THE ": int" AND "-> None" BITS YOU'LL SEE EVERYWHERE
These are "type hints". They say what kind of value a variable holds:
    speed: float = 0.0                    speed holds a decimal number
    def add(a: int, b: int) -> int:       add takes two whole numbers and gives back a whole number
    def jump(self) -> None:               jump doesn't give anything back
Python ignores type hints when it runs the game. They are notes for people,
and VS Code uses them to spot mistakes and suggest names as you type.

The types you'll see most:
    int         a whole number, like 3 or -10
    float       a decimal number, like 2.5
    str         text, like "PLAY"
    bool        True or False
    list[str]   a list where every item is text, like ["PLAY", "QUIT"]
    tuple[int, int]   a pair of whole numbers, like (4, 7)
    None        nothing
    Player, Level, Camera...   our own classes, defined in the other files
"""

import time

import pygame

from camera import Camera
from game import Game
from input_handler import handle_key_press, handle_key_release, handle_held_keys
from level import Level
from player import Player
from render import Renderer

# Where the player appears at the start of a level, and after dying.
SPAWN_X: float = 10.0
SPAWN_Y: float = 5.0

# If a frame takes longer than this (e.g. the window was dragged), pretend it
# only took this long. Otherwise the player could jump straight through a wall.
MAX_FRAME_TIME: float = 0.05

FRAMES_PER_SECOND: int = 240


def main() -> None:
    pygame.init()
    renderer: Renderer = Renderer()
    clock: pygame.time.Clock = pygame.time.Clock()

    game: Game = Game()
    camera: Camera = Camera()
    player: Player = Player(SPAWN_X, SPAWN_Y)
    # Start with level 1 loaded. It gets replaced when the player picks a level.
    level: Level = Level(0)

    # time.perf_counter() gives the current time in seconds, as a float.
    last_time: float = time.perf_counter()

    while game.running:
        # 1. Handle events: the window's close button and key presses.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                handle_key_press(game, player, event.key)
            elif event.type == pygame.KEYUP:
                handle_key_release(game, player, event.key)

        # 2. Work out dt ("delta time"): how many seconds since the last frame.
        #    It's usually a tiny number like 0.004. We move things by speed * dt,
        #    so the game runs at the same speed on fast and slow computers.
        now: float = time.perf_counter()
        dt: float = now - last_time
        last_time = now
        if dt > MAX_FRAME_TIME:
            dt = MAX_FRAME_TIME

        # Pause everything while the window isn't selected.
        if not pygame.key.get_focused():
            clock.tick(30)
            continue

        # 3. Update and draw whichever screen we're on.
        if game.state == "menu":
            renderer.draw_main_menu(game)

        elif game.state == "level_select":
            renderer.draw_level_select(game)
            if game.start_level_requested:
                game.start_level_requested = False
                level = Level(game.level_selected)
                player.respawn(SPAWN_X, SPAWN_Y)
                game.state = "playing"

        elif game.state == "playing":
            handle_held_keys(game, player, dt)
            player.update(level, dt)

            if player.touching_spike(level) or player.fell_off_level(level):
                player.respawn(SPAWN_X, SPAWN_Y)
            elif player.touching_goal(level):
                game.levels_completed[game.level_selected] = True
                game.state = "level_complete"

            camera.update(player, dt)
            renderer.draw_level(level, player, camera)

        elif game.state == "paused":
            renderer.draw_pause_menu(game)

        elif game.state == "level_complete":
            renderer.draw_level_complete()

        elif game.state == "editor":
            renderer.draw_editor()

        # 4. Show what we just drew, then wait so we don't run faster than FRAMES_PER_SECOND.
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)

    pygame.quit()


# This means "only start the game if this file was run directly",
# not if another file imports it.
if __name__ == "__main__":
    main()
