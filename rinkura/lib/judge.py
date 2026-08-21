from sonolus.script.bucket import Judgment

PERFECT_PLUS = 5
PERFECT = 4
GREAT = 3
GOOD = 2
BAD = 1
MISS = 0

TAP_WINDOWS = {
    PERFECT_PLUS: 0.025,
    GREAT: 0.04,
    GOOD: 0.07,
    BAD: 0.1,
}

FLICK_MIN_DIFF = 0.07
FLICK_MAX_DIFF = 0.1
FLICK_VALID_TIME = 0.075
FLICK_DISTANCE = 625
FLICK_DISTANCE_NORMALIZED = 0.002143

HOLD_MIN_DIFF = 0.04
HOLD_MAX_DIFF = 0.125
HOLD_END_MIN_DIFF = -0.1
HOLD_END_MAX_DIFF = 0.0

TRACE_WINDOW = 0.07

COMBO_MIN_JUDGMENT = GOOD


def judge_tap(diff: float) -> int:
    abs_diff = abs(diff)
    if abs_diff <= TAP_WINDOWS[PERFECT_PLUS]:
        return PERFECT_PLUS
    if abs_diff <= TAP_WINDOWS[GREAT]:
        return PERFECT
    if abs_diff <= TAP_WINDOWS[GOOD]:
        return GREAT
    if abs_diff <= TAP_WINDOWS[BAD]:
        return GOOD
    return MISS

def judge_flick(diff: float) -> int:
    abs_diff = round(abs(diff), 3)
    if abs_diff <= FLICK_MIN_DIFF:
        return PERFECT_PLUS
    if abs_diff <= FLICK_MAX_DIFF:
        return GREAT
    return MISS

def continues_combo(judgment: int) -> bool:
    return judgment >= COMBO_MIN_JUDGMENT


def to_sonolus_judgment(judgment: int) -> Judgment:
    if judgment >= PERFECT:
        return Judgment.PERFECT
    if judgment == GREAT:
        return Judgment.GREAT
    if judgment == GOOD:
        return Judgment.GOOD
    return Judgment.MISS