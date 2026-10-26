"""The player (the red square): running, jumping, gravity and bumping into blocks.

IMPORTANT: on computer screens, y goes DOWN as it gets bigger.
  y = 0 is the top of the level, and bigger y is further down.
  So a negative speed_y means moving UP, and a positive speed_y means falling.
"""

from level import BLOCK, SPIKE, GOAL, TILE_SIZE

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16

# Speeds are in pixels per second. Accelerations are in pixels per second, per second.
GRAVITY = 2200.0
FALLING_GRAVITY_MULTIPLIER = 1.5  # fall faster than you rise, which feels snappier
RUN_ACCELERATION = 1900.0
AIR_CONTROL = 0.5                 # you can only steer half as well in the air
FRICTION = 1500.0                 # how quickly you slow down on the ground
MAX_RUN_SPEED = 300.0
JUMP_SPEED = -550.0               # negative because up is negative y
JUMP_CUT = 0.5                    # letting go of jump early halves your upward speed

# Two tricks that make jumping feel fair. Most platform games use them.
# "Coyote time": you can still jump for 0.1 seconds after running off a ledge,
# like a cartoon coyote that runs off a cliff and doesn't fall straight away.
COYOTE_TIME = 0.1
# "Jump buffer": if you press jump up to 0.1 seconds BEFORE you land,
# the game remembers and jumps as soon as you touch the ground.
JUMP_BUFFER_TIME = 0.1


def move_towards(current, target, step):
    """Change current by up to `step`, getting closer to target without going past it."""
    if current < target:
        current = current + step
        if current > target:
            current = target
    elif current > target:
        current = current - step
        if current < target:
            current = target
    return current


# A class is a way of keeping some variables and the functions that use them together.
# Inside the class, "self" means "this player", so self.x is this player's x position.
class Player:
    # __init__ runs automatically when we make a player with Player(x, y).
    def __init__(self, x, y):
        self.respawn(x, y)

    def respawn(self, x, y):
        """Put the player at (x, y), standing still, with all jump timers cleared."""
        self.x = x
        self.y = y
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.on_ground = False
        self.coyote_timer = 0.0
        self.jump_buffer_timer = 0.0
        self.jump_held = False
        self.jump_already_cut = False

    # ---- Called by the controls ----

    def press_jump(self):
        # Don't jump straight away: start the buffer timer, and update() jumps
        # as soon as the player is allowed to.
        self.jump_buffer_timer = JUMP_BUFFER_TIME
        self.jump_held = True
        self.jump_already_cut = False

    def release_jump(self):
        self.jump_held = False

    def run_left(self, dt):
        steering = 1.0
        if not self.on_ground:
            steering = AIR_CONTROL
        self.speed_x = move_towards(self.speed_x, -MAX_RUN_SPEED, RUN_ACCELERATION * dt * steering)

    def run_right(self, dt):
        steering = 1.0
        if not self.on_ground:
            steering = AIR_CONTROL
        self.speed_x = move_towards(self.speed_x, MAX_RUN_SPEED, RUN_ACCELERATION * dt * steering)

    # ---- Called once per frame ----

    def update(self, level, dt):
        """Move the player forward by dt seconds. The order of these steps matters."""
        self.on_ground = False
        self.apply_gravity(dt)
        self.cut_jump_if_released()
        self.jump_if_allowed()
        self.move_horizontally(level, dt)
        self.move_vertically(level, dt)
        self.apply_friction(dt)
        self.update_coyote_timer(dt)
        self.update_jump_buffer_timer(dt)

    def apply_gravity(self, dt):
        strength = GRAVITY
        if self.speed_y > 0:  # falling
            strength = GRAVITY * FALLING_GRAVITY_MULTIPLIER
        self.speed_y = self.speed_y + strength * dt

    def cut_jump_if_released(self):
        # Short tap = small jump, hold = big jump.
        moving_up = self.speed_y < 0
        if moving_up and not self.jump_held and not self.jump_already_cut:
            self.speed_y = self.speed_y * JUMP_CUT
            self.jump_already_cut = True

    def jump_if_allowed(self):
        can_jump = self.on_ground or self.coyote_timer > 0
        wants_to_jump = self.jump_buffer_timer > 0
        if can_jump and wants_to_jump:
            self.speed_y = JUMP_SPEED
            self.on_ground = False
            self.coyote_timer = 0.0
            self.jump_buffer_timer = 0.0

    def move_horizontally(self, level, dt):
        self.x = self.x + self.speed_x * dt

        block = self.find_block_overlapping_player(level)
        if block is None:
            return

        # We moved into a block, so push the player back out to its edge and stop.
        block_column, block_row = block
        if self.speed_x > 0:    # was moving right, so stop at the block's left side
            self.x = block_column * TILE_SIZE - PLAYER_WIDTH
        elif self.speed_x < 0:  # was moving left, so stop at the block's right side
            self.x = (block_column + 1) * TILE_SIZE
        self.speed_x = 0.0

    def move_vertically(self, level, dt):
        self.y = self.y + self.speed_y * dt
        self.on_ground = False

        block = self.find_block_overlapping_player(level)
        if block is None:
            return

        block_column, block_row = block
        if self.speed_y > 0:    # was falling, so land on top of the block
            self.y = block_row * TILE_SIZE - PLAYER_HEIGHT
            self.on_ground = True
            self.jump_already_cut = False
        elif self.speed_y < 0:  # was rising, so bump our head on the block's underside
            self.y = (block_row + 1) * TILE_SIZE
        self.speed_y = 0.0

    def find_block_overlapping_player(self, level):
        """Return (column, row) of the first block the player overlaps, or None if there isn't one."""
        # Work out which tiles the player's square covers.
        # Dividing a position by TILE_SIZE (16) and rounding down with int()
        # turns a pixel position into a tile number, e.g. x = 40 is in column 2.
        # The 0.01 stops a player who is exactly touching the next tile from
        # counting as inside it.
        left_column = int(self.x / TILE_SIZE)
        right_column = int((self.x + PLAYER_WIDTH - 0.01) / TILE_SIZE)
        top_row = int(self.y / TILE_SIZE)
        bottom_row = int((self.y + PLAYER_HEIGHT - 0.01) / TILE_SIZE)

        for row in range(top_row, bottom_row + 1):
            for column in range(left_column, right_column + 1):
                if level.get_tile(column, row) == BLOCK:
                    return (column, row)
        return None

    def apply_friction(self, dt):
        if not self.on_ground:
            return
        if self.speed_x > 0:
            self.speed_x = self.speed_x - FRICTION * dt
            if self.speed_x < 0:
                self.speed_x = 0.0
        elif self.speed_x < 0:
            self.speed_x = self.speed_x + FRICTION * dt
            if self.speed_x > 0:
                self.speed_x = 0.0

    def update_coyote_timer(self, dt):
        if self.on_ground:
            self.coyote_timer = COYOTE_TIME
        else:
            self.coyote_timer = self.coyote_timer - dt
            if self.coyote_timer < 0:
                self.coyote_timer = 0.0

    def update_jump_buffer_timer(self, dt):
        self.jump_buffer_timer = self.jump_buffer_timer - dt
        if self.jump_buffer_timer < 0:
            self.jump_buffer_timer = 0.0

    # ---- Questions main.py asks each frame ----

    def tile_at_centre(self, level):
        """Return the tile under the middle of the player."""
        centre_x = self.x + PLAYER_WIDTH // 2
        centre_y = self.y + PLAYER_HEIGHT // 2
        column = int(centre_x / TILE_SIZE)
        row = int(centre_y / TILE_SIZE)
        return level.get_tile(column, row)

    def touching_spike(self, level):
        return self.tile_at_centre(level) == SPIKE

    def touching_goal(self, level):
        return self.tile_at_centre(level) == GOAL

    def fell_off_level(self, level):
        level_bottom = level.height * TILE_SIZE
        return self.y >= level_bottom
