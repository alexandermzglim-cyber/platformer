CAMERA_FOLLOW_SPEED = 5.0


class Camera:
    def __init__(self, zoom, window_w, window_h):
        self.x = 0.0
        self.y = 0.0
        self.zoom = zoom
        self.zone_w = window_w / 4.0
        self.zone_h = window_h / 6.0

    def update(self, player, window_w, window_h, dt):
        left = self.x + (window_w - self.zone_w) / 2 / self.zoom
        right = left + self.zone_w / self.zoom
        top = self.y + (window_h - self.zone_h) / 2 / self.zoom
        bottom = top + self.zone_h / self.zoom

        target_x = self.x
        if player.x < left:
            target_x -= left - player.x
        if player.x > right:
            target_x += player.x - right

        target_y = self.y
        if player.y < top:
            target_y -= top - player.y
        if player.y > bottom:
            target_y += player.y - bottom

        self.x += (target_x - self.x) * dt * CAMERA_FOLLOW_SPEED
        self.y += (target_y - self.y) * dt * CAMERA_FOLLOW_SPEED
