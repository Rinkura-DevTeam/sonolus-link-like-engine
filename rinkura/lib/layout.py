import math

from sonolus.script.quad import Quad, Rect
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

JUDGE_LINE_Y = -0.49

NOTE_SPAWN_MARGIN = 0.02

STAGE_APEX_Y = 1.1426

NOTE_WIDTH_SUB = 6.0
NOTE_WIDTH_SCALE = 0.2
NOTE_WIDTH_OFFSET = 1.15
NOTE_HEIGHT_AT_JUDGE = 0.196


def get_fov_vertical(fov: float, aspect_ratio: float) -> float:
    return 2 * math.degrees(
        math.atan(math.tan(math.radians(fov * 0.5)) / aspect_ratio)
    )


def stage_half_width() -> float:
    return aspect_ratio() * 0.688


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


EASE_BASE = 1.06
EASE_EXP = 45


def ease(x: float) -> float:
    x = max(x, 0.0)
    value = EASE_BASE ** (EASE_EXP * (x - 1))
    from_min = EASE_BASE ** -EASE_EXP
    from_max = EASE_BASE
    return (value - from_min) / (from_max - from_min) * EASE_BASE


def note_world_width(width_raw: float) -> float:
    return max((width_raw - NOTE_WIDTH_SUB) * NOTE_WIDTH_SCALE + NOTE_WIDTH_OFFSET, 0.3)


def project(world_x: float, t: float, width_raw: float = 10.0) -> tuple[float, float, float, float]:
    t = max(min(t, 1.1), 0.0)
    e = ease(t)

    spawn_y = 1.0 + NOTE_SPAWN_MARGIN
    half = stage_half_width()
    world_to_screen = half / WORLD_HALF_WIDTH

    screen_x = (world_x / WORLD_HALF_WIDTH) * half * e
    screen_y = spawn_y + (JUDGE_LINE_Y - spawn_y) * e

    screen_w = note_world_width(width_raw) * world_to_screen * e
    screen_h = NOTE_HEIGHT_AT_JUDGE * e

    return screen_x, screen_y, screen_w, screen_h


def note_quad(center_x: float, center_y: float, width: float, height: float) -> Rect:
    return Rect.from_center(
        center=Vec2(center_x, center_y),
        dimensions=Vec2(width, height),
    )


def line_quad(a: Vec2, b: Vec2, thickness: float) -> Quad:
    direction = (b - a).normalize()
    perp = direction.orthogonal() * (thickness / 2)
    return Quad(
        bl=a - perp,
        tl=a + perp,
        tr=b + perp,
        br=b - perp,
    )


def stage_apex() -> Vec2:
    return Vec2(0.0, STAGE_APEX_Y)


def stage_left_corner() -> Vec2:
    return Vec2(-stage_half_width(), JUDGE_LINE_Y)


def stage_right_corner() -> Vec2:
    return Vec2(stage_half_width(), JUDGE_LINE_Y)


def raw_to_middle_x(raw_left: float, raw_right: float) -> float:
    return (raw_left + raw_right) / 2


def mirror_raw(raw_value: int) -> int:
    return 59 - raw_value

ARROW_SIZE_SCALE = 2.921875
ARROW_GAP = 0.03
ARROW_ROTATION_DEG = 0.0



def flick_arrow_quad(center_x: float, center_y: float, note_width: float, note_height: float) -> Quad:
    size = note_height * ARROW_SIZE_SCALE
    cx = center_x
    cy = center_y + note_height / 2 + ARROW_GAP

    angle = math.radians(ARROW_ROTATION_DEG)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    right = Vec2(cos_a, sin_a) * (size / 2)
    up = Vec2(-sin_a, cos_a) * (size / 2)
    center = Vec2(cx, cy)

    return Quad(
        bl=center - right - up,
        tl=center - right + up,
        tr=center + right + up,
        br=center + right - up,
    )
