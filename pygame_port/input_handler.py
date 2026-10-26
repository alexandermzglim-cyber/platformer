import pygame

from game import (
    State, MENU_PLAY, MENU_EDITOR, MENU_QUIT, MENU_COUNT,
    PAUSE_RESUME, PAUSE_LEVEL_SELECT, PAUSE_MAIN_MENU, PAUSE_QUIT, PAUSE_COUNT,
)

JUMP_KEYS = (pygame.K_SPACE, pygame.K_w)


def handle_key_event(game, player, event):
    if game.state == State.PLAYING:
        _playing(game, player, event)
        return
    if event.type != pygame.KEYDOWN:
        return
    if game.state == State.MENU:
        _main_menu(game, event.key)
    elif game.state == State.LEVEL_SELECT:
        _level_select(game, event.key)
    elif game.state == State.PAUSED:
        _pause_menu(game, event.key)
    elif game.state == State.EDITOR:
        if event.key == pygame.K_ESCAPE:
            game.state = State.MENU
    elif game.state == State.LEVEL_COMPLETE:
        if event.key == pygame.K_RETURN:
            game.state = State.LEVEL_SELECT


def update_held_keys(game, player, dt):
    if game.state != State.PLAYING:
        return
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move_left(dt)
    if keys[pygame.K_d]:
        player.move_right(dt)


def _playing(game, player, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game.state = State.PAUSED
        elif event.key in JUMP_KEYS:
            player.jump()
    elif event.type == pygame.KEYUP and event.key in JUMP_KEYS:
        player.release_jump()


def _main_menu(game, key):
    if key == pygame.K_UP:
        game.main_menu_selected = (game.main_menu_selected - 1) % MENU_COUNT
    elif key == pygame.K_DOWN:
        game.main_menu_selected = (game.main_menu_selected + 1) % MENU_COUNT
    elif key == pygame.K_RETURN:
        if game.main_menu_selected == MENU_PLAY:
            game.state = State.LEVEL_SELECT
        elif game.main_menu_selected == MENU_EDITOR:
            game.state = State.EDITOR
        elif game.main_menu_selected == MENU_QUIT:
            game.running = False


def _level_select(game, key):
    if key == pygame.K_UP:
        game.level_selected = (game.level_selected - 1) % game.level_count
    elif key == pygame.K_DOWN:
        game.level_selected = (game.level_selected + 1) % game.level_count
    elif key == pygame.K_RETURN:
        game.level_confirmation = True
    elif key == pygame.K_ESCAPE:
        game.state = State.MENU


def _pause_menu(game, key):
    if key == pygame.K_UP:
        game.pause_selected = (game.pause_selected - 1) % PAUSE_COUNT
    elif key == pygame.K_DOWN:
        game.pause_selected = (game.pause_selected + 1) % PAUSE_COUNT
    elif key == pygame.K_RETURN:
        if game.pause_selected == PAUSE_RESUME:
            game.state = State.PLAYING
        elif game.pause_selected == PAUSE_LEVEL_SELECT:
            game.state = State.LEVEL_SELECT
        elif game.pause_selected == PAUSE_MAIN_MENU:
            game.state = State.MENU
        elif game.pause_selected == PAUSE_QUIT:
            game.running = False
    elif key == pygame.K_ESCAPE:
        game.state = State.PLAYING
