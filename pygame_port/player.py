from level import TILE_SOLID, TILE_SPIKE, TILE_GOAL

TILE_SIZE = 16
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16

GRAVITY = 2200.0
FALL_GRAVITY_MULTIPLIER = 1.5
MOVEMENT_ACCELERATION = 1900.0
AIR_CONTROL_MULTIPLIER = 0.5
FRICTION = 1500.0
MAXIMUM_SPEED = 300.0
JUMP_VELOCITY = -550.0
JUMP_CUT_MULTIPLIER = 0.5
COYOTE_TIME = 0.1
JUMP_BUFFER_TIME = 0.1


def smooth_approach(current, target, step):
    if current < target:
        return min(current + step, target)
    if current > target:
        return max(current - step, target)
    return current


class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.ground = False
        self.coyote_time = 0.0
        self.buffer_time = 0.0
        self.jump_held = False
        self.jump_cut = False

    def jump(self):
        self.buffer_time = JUMP_BUFFER_TIME
        self.jump_held = True
        self.jump_cut = False

    def release_jump(self):
        self.jump_held = False

    def move_left(self, dt):
        multiplier = 1.0 if self.ground else AIR_CONTROL_MULTIPLIER
        self.vx = smooth_approach(self.vx, -MAXIMUM_SPEED, MOVEMENT_ACCELERATION * dt * multiplier)

    def move_right(self, dt):
        multiplier = 1.0 if self.ground else AIR_CONTROL_MULTIPLIER
        self.vx = smooth_approach(self.vx, MAXIMUM_SPEED, MOVEMENT_ACCELERATION * dt * multiplier)

    def update(self, level, dt):
        self.ground = False
        self._apply_gravity(dt)
        self._variable_jump()
        self._jump_buffer()
        self._collide_x(level, dt)
        self._collide_y(level, dt)
        self._apply_friction(dt)
        self._update_coyote_time(dt)
        self.buffer_time = max(self.buffer_time - dt, 0.0)

    def on_spike(self, level):
        return level.tile(*self._centre_tile()) == TILE_SPIKE

    def fell_off_level(self, level):
        return self.y >= level.height * TILE_SIZE

    def on_goal(self, level):
        return level.tile(*self._centre_tile()) == TILE_GOAL

    def _centre_tile(self):
        centre_x = self.x + PLAYER_WIDTH // 2
        centre_y = self.y + PLAYER_HEIGHT // 2
        return int(centre_x / TILE_SIZE), int(centre_y / TILE_SIZE)

    def _apply_gravity(self, dt):
        multiplier = FALL_GRAVITY_MULTIPLIER if self.vy > 0 else 1.0
        self.vy += GRAVITY * dt * multiplier

    def _variable_jump(self):
        if not self.jump_held and self.vy < 0 and not self.jump_cut:
            self.vy *= JUMP_CUT_MULTIPLIER
            self.jump_cut = True

    def _jump_buffer(self):
        if (self.ground or self.coyote_time > 0.0) and self.buffer_time > 0.0:
            self.vy = JUMP_VELOCITY
            self.ground = False
            self.coyote_time = 0.0
            self.buffer_time = 0.0

    def _tile_bounds(self):
        tile_left = int(self.x / TILE_SIZE)
        tile_right = int((self.x + PLAYER_WIDTH - 0.01) / TILE_SIZE)
        tile_top = int(self.y / TILE_SIZE)
        tile_bottom = int((self.y + PLAYER_HEIGHT - 0.01) / TILE_SIZE)
        return tile_left, tile_right, tile_top, tile_bottom

    def _collide_x(self, level, dt):
        self.x += self.vx * dt
        tile_left, tile_right, tile_top, tile_bottom = self._tile_bounds()
        for ty in range(tile_top, tile_bottom + 1):
            for tx in range(tile_left, tile_right + 1):
                if level.tile(tx, ty) != TILE_SOLID:
                    continue
                if self.vx > 0:
                    self.x = tx * TILE_SIZE - PLAYER_WIDTH
                elif self.vx < 0:
                    self.x = (tx + 1) * TILE_SIZE
                self.vx = 0.0
                break
            if self.vx == 0:
                break

    def _collide_y(self, level, dt):
        self.y += self.vy * dt
        self.ground = False
        tile_left, tile_right, tile_top, tile_bottom = self._tile_bounds()
        for ty in range(tile_top, tile_bottom + 1):
            for tx in range(tile_left, tile_right + 1):
                if level.tile(tx, ty) != TILE_SOLID:
                    continue
                if self.vy > 0:
                    self.y = ty * TILE_SIZE - PLAYER_HEIGHT
                    self.ground = True
                    self.jump_cut = False
                elif self.vy < 0:
                    self.y = (ty + 1) * TILE_SIZE
                self.vy = 0.0
                break
            if self.vy == 0:
                break

    def _apply_friction(self, dt):
        if not self.ground:
            return
        if self.vx > 0:
            self.vx = max(self.vx - FRICTION * dt, 0.0)
        elif self.vx < 0:
            self.vx = min(self.vx + FRICTION * dt, 0.0)

    def _update_coyote_time(self, dt):
        if self.ground:
            self.coyote_time = COYOTE_TIME
        else:
            self.coyote_time = max(self.coyote_time - dt, 0.0)
