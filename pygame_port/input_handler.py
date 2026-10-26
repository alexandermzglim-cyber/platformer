"""Keyboard controls.

Menus react to single key presses. Running reacts to keys being held down,
so it's checked every frame instead (see handle_held_keys).
"""

import pygame

from game import LEVEL_COUNT, MAIN_MENU_OPTIONS, PAUSE_MENU_OPTIONS, move_selection


def is_jump_key(key):
    return key == pygame.K_SPACE or key == pygame.K_w or key == pygame.K_UP


def handle_key_press(game, player, key):
    """Called once each time a key goes down."""
    if game.state == "playing":
        if key == pygame.K_ESCAPE:
            game.state = "paused"
        elif is_jump_key(key):
            player.press_jump()

    elif game.state == "menu":
        if key == pygame.K_UP:
            game.main_menu_selected = move_selection(game.main_menu_selected, -1, len(MAIN_MENU_OPTIONS))
        elif key == pygame.K_DOWN:
            game.main_menu_selected = move_selection(game.main_menu_selected, +1, len(MAIN_MENU_OPTIONS))
        elif key == pygame.K_RETURN:
            choice = MAIN_MENU_OPTIONS[game.main_menu_selected]
            if choice == "PLAY":
                game.state = "level_select"
            elif choice == "EDITOR":
                game.state = "editor"
            elif choice == "QUIT":
                game.running = False

    elif game.state == "level_select":
        if key == pygame.K_UP:
            game.level_selected = move_selection(game.level_selected, -1, LEVEL_COUNT)
        elif key == pygame.K_DOWN:
            game.level_selected = move_selection(game.level_selected, +1, LEVEL_COUNT)
        elif key == pygame.K_RETURN:
            game.start_level_requested = True
        elif key == pygame.K_ESCAPE:
            game.state = "menu"

    elif game.state == "paused":
        if key == pygame.K_UP:
            game.pause_menu_selected = move_selection(game.pause_menu_selected, -1, len(PAUSE_MENU_OPTIONS))
        elif key == pygame.K_DOWN:
            game.pause_menu_selected = move_selection(game.pause_menu_selected, +1, len(PAUSE_MENU_OPTIONS))
        elif key == pygame.K_ESCAPE:
            game.state = "playing"
        elif key == pygame.K_RETURN:
            choice = PAUSE_MENU_OPTIONS[game.pause_menu_selected]
            if choice == "RESUME":
                game.state = "playing"
            elif choice == "LEVEL_SELECT":
                game.state = "level_select"
            elif choice == "MAIN MENU":
                game.state = "menu"
            elif choice == "QUIT":
                game.running = False

    elif game.state == "level_complete":
        if key == pygame.K_RETURN:
            game.state = "level_select"

    elif game.state == "editor":
        if key == pygame.K_ESCAPE:
            game.state = "menu"


def handle_key_release(game, player, key):
    """Called once each time a key comes back up."""
    if game.state == "playing" and is_jump_key(key):
        player.release_jump()


def handle_held_keys(game, player, dt):
    """Called every frame. Runs left or right while A/D or the left/right arrow keys are held down."""
    if game.state != "playing":
        return
    keys_held = pygame.key.get_pressed()
    if keys_held[pygame.K_a] or keys_held[pygame.K_LEFT]:
        player.run_left(dt)
    if keys_held[pygame.K_d] or keys_held[pygame.K_RIGHT]:
        player.run_right(dt)
