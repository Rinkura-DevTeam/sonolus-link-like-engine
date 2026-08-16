import math

from sonolus.script.quad import Rect
from sonolus.script.vec import Vec2

A = 0.072
B = 3.9

SPAWN_Z = 52.0
BORDER_Z = -4.632
LANE_WIDTH = 0.15
NOTE_JUDGEMENT_FRONT_Z = -3.91
NOTE_JUDGEMENT_BACK_Z = -5.25

BASE_WIDTH = 1920
BASE_HEIGHT = 1080
BASE_ASPECT = BASE_WIDTH / BASE_HEIGHT

BASE_FOV = 60.0

LANE_PIVOT = 29.5
LANE0_CENTER = -LANE_PIVOT * LANE_WIDTH
WORLD_HALF_WIDTH = LANE_PIVOT * LANE_WIDTH

JUDGE_LINE_Y = -0.82
SPAWN_POINT_Y = 0.7
STAGE_HALF_WIDTH = 0.85

MIN_NOTE_SIZE = 0.05
MAX_NOTE_SIZE = 0.22

APPROACH_SCALE = 1.06**-45


def get_fov_vertical(fov: float, aspect_ratio: float) -> float:
    return 2 * math.degrees(
        math.atan(math.tan(math.radians(fov * 0.5)) / aspect_ratio)
    )


def get_world_z(elapsed: float, duration: float, speed: float, n: float = 0.0) -> float:
    t = (duration - elapsed) * speed
    return BORDER_Z + (B * t) + (A * t**3) - n


def solve_fall_duration(speed: float = 1.0) -> float:
    target = SPAWN_Z - BORDER_Z
    t = 5.0
    for _ in range(50):
        f = B * t + A * t**3 - target
        fprime = B + 3 * A * t**2
        t = t - f / fprime
    safe_speed = max(speed, 1e-6)
    return t / safe_speed


def get_world_x(middle_x: float) -> float:
    return LANE0_CENTER + LANE_WIDTH * middle_x


def approach_curve(progress: float) -> float:
    clamped = min(max(progress, 0.0), 1.0)
    return APPROACH_SCALE ** (1 - clamped)


def z_progress(world_z: float) -> float:
    return (SPAWN_Z - world_z) / (SPAWN_Z - BORDER_Z)


def project(world_x: float, world_z: float) -> tuple[float, float, float]:
    progress = z_progress(world_z)
    curve = approach_curve(progress)

    screen_x = (world_x / WORLD_HALF_WIDTH) * STAGE_HALF_WIDTH * curve
    screen_y = SPAWN_POINT_Y + (JUDGE_LINE_Y - SPAWN_POINT_Y) * curve
    size = MIN_NOTE_SIZE + (MAX_NOTE_SIZE - MIN_NOTE_SIZE) * curve

    return screen_x, screen_y, size


def note_quad(center_x: float, center_y: float, size: float) -> Rect:
    return Rect.from_center(
        center=Vec2(center_x, center_y),
        dimensions=Vec2(size, size),
    )


def raw_to_middle_x(raw_left: float, raw_right: float) -> float:
    return (raw_left + raw_right) / 2


def mirror_raw(raw_value: int) -> int:
    return 59 - raw_value
