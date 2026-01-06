import math


def normalize_screen(x, y, screen_w, screen_h):
    nx = (x / screen_w) * 2.0 - 1.0
    ny = (y / screen_h) * 2.0 - 1.0
    return nx, ny


def screen_to_world(nx, ny, cam, screen_w, screen_h):
    world_x = cam.position[0] + nx * (screen_w / 2) / cam.zoom
    world_y = cam.position[1] + ny * (screen_h / 2) / cam.zoom
    return world_x, world_y


def normalized_direction(from_x, from_y, to_x, to_y):
    dx = to_x - from_x
    dy = to_y - from_y

    length = math.hypot(dx, dy)
    if length == 0:
        return 0.0, 1.0  # смотрим вверх по умолчанию

    return dx / length, dy / length


def angle_from_dir(nx, ny):
    return math.degrees(math.atan2(nx, ny))
