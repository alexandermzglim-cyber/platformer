"""The camera decides which part of the level you can see.

Imagine an invisible box in the middle of the screen. While the player is
inside the box, the camera stays still. When the player walks out of the box,
the camera slides along to follow them. This stops the screen jiggling every
time the player moves a tiny bit. Game makers call this box a "dead zone".
"""

from game import GAME_WIDTH, GAME_HEIGHT

ZOOM = 2.5               # draw the level 2.5 times bigger than its real size
FOLLOW_SPEED = 5.0       # higher = camera catches up faster
DEAD_ZONE_WIDTH = GAME_WIDTH / 4
DEAD_ZONE_HEIGHT = GAME_HEIGHT / 6


class Camera:
    def __init__(self):
        # The world position shown at the top-left corner of the screen.
        self.x = 0.0
        self.y = 0.0
        self.zoom = ZOOM

    def update(self, player, dt):
        # Where the invisible box is right now, measured in level pixels.
        # (The screen is zoomed in, so we divide by zoom to turn screen sizes into level sizes.)
        box_left = self.x + (GAME_WIDTH - DEAD_ZONE_WIDTH) / 2 / self.zoom
        box_right = box_left + DEAD_ZONE_WIDTH / self.zoom
        box_top = self.y + (GAME_HEIGHT - DEAD_ZONE_HEIGHT) / 2 / self.zoom
        box_bottom = box_top + DEAD_ZONE_HEIGHT / self.zoom

        # Work out where the camera needs to be to put the player back in the box.
        target_x = self.x
        if player.x < box_left:
            target_x = target_x - (box_left - player.x)
        if player.x > box_right:
            target_x = target_x + (player.x - box_right)

        target_y = self.y
        if player.y < box_top:
            target_y = target_y - (box_top - player.y)
        if player.y > box_bottom:
            target_y = target_y + (player.y - box_bottom)

        # Move only part of the way there each frame, so the camera glides smoothly.
        self.x = self.x + (target_x - self.x) * dt * FOLLOW_SPEED
        self.y = self.y + (target_y - self.y) * dt * FOLLOW_SPEED
