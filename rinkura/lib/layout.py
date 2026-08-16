import math

from sonolus.script.quad import Rect
from sonolus.script.runtime import aspect_ratio
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

JUDGE_LINE_Y = -0.6

NOTE_RADIUS_MIN = 0.02
NOTE_RADIUS_MAX = 0.075

NOTE_WIDTH_SUB = 6.0
NOTE_WIDTH_SCALE = 0.2
NOTE_WIDTH_OFFSET = 1.15
NOTE_HEIGHT_RATIO = 0.4


def get_fov_vertical(fov: float, aspect_ratio: float) -> float:
    return 2 * math.degrees(
        math.atan(math.tan(math.radians(fov * 0.5)) / aspect_ratio)
    )


def stage_half_width() -> float:
    return aspect_ratio() * 0.68


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


def size_curve(t: float) -> float:
    clamped = min(max(t, 0.0), 1.0)
    return clamped**2


def note_world_width(width_raw: float) -> float:
    return max((width_raw - NOTE_WIDTH_SUB) * NOTE_WIDTH_SCALE + NOTE_WIDTH_OFFSET, 0.3)


def project(world_x: float, t: float, width_raw: float = 10.0) -> tuple[float, float, float, float]:
    t = min(max(t, 0.0), 1.0)
    grow = size_curve(t)

    spawn_y = 1.0 + NOTE_RADIUS_MIN
    half = stage_half_width()
    world_to_screen = half / WORLD_HALF_WIDTH

    screen_x = (world_x / WORLD_HALF_WIDTH) * half * t
    screen_y = spawn_y + (JUDGE_LINE_Y - spawn_y) * t

    screen_w = note_world_width(width_raw) * world_to_screen * grow
    screen_h = max(screen_w * NOTE_HEIGHT_RATIO, 2 * NOTE_RADIUS_MIN * grow)

    return screen_x, screen_y, screen_w, screen_h


def note_quad(center_x: float, center_y: float, width: float, height: float) -> Rect:
    return Rect.from_center(
        center=Vec2(center_x, center_y),
        dimensions=Vec2(width, height),
    )


def raw_to_middle_x(raw_left: float, raw_right: float) -> float:
    return (raw_left + raw_right) / 2


def mirror_raw(raw_value: int) -> int:
    return 59 - raw_value
