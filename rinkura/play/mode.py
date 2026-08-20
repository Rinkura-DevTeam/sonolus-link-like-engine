from sonolus.script.archetype import (
    HapticType,
    PlayArchetype,
    callback,
    entity_memory,
    imported,
)
from sonolus.script.bucket import Judgment, JudgmentWindow
from sonolus.script.engine import PlayMode
from sonolus.script.interval import Interval
from sonolus.script.runtime import time, touches

from rinkura.lib import judge, layout
from rinkura.lib.buckets import Buckets
from rinkura.lib.options import Options
from rinkura.lib.skin import Skin
from rinkura.play.stage import Stage


class TapNote(PlayArchetype):
    name = "TapNote"

    is_scored = True

    beat: float = imported(name="beat")
    l1_raw: float = imported(name="l1")
    r1_raw: float = imported(name="r1")

    visual_time_min: float = entity_memory()
    visual_time_max: float = entity_memory()

    target_time: float = entity_memory()
    duration: float = entity_memory()
    speed: float = entity_memory()
    middle_x: float = entity_memory()
    world_x: float = entity_memory()
    width_raw: float = entity_memory()
    n_offset: float = entity_memory()

    note_judgment: int = entity_memory()

    @callback(order=1)
    def preprocess(self):
        Buckets.tap.window = JudgmentWindow(
            perfect=Interval(-judge.TAP_WINDOWS[judge.GREAT], judge.TAP_WINDOWS[judge.GREAT]),
            great=Interval(-judge.TAP_WINDOWS[judge.GOOD], judge.TAP_WINDOWS[judge.GOOD]),
            good=Interval(-judge.TAP_WINDOWS[judge.BAD], judge.TAP_WINDOWS[judge.BAD]),
        )
        self.target_time = self.beat
        self.speed = Options.speed
        self.duration = layout.solve_fall_duration(self.speed)
        self.visual_time_max = self.target_time
        self.visual_time_min = self.target_time - self.duration
        self.n_offset = 0.0

        self.middle_x = layout.raw_to_middle_x(self.l1_raw, self.r1_raw)
        self.world_x = layout.get_world_x(self.middle_x)
        self.width_raw = self.r1_raw - self.l1_raw

        self.note_judgment = judge.MISS

    def spawn_order(self) -> float:
        return self.visual_time_min

    def should_spawn(self) -> bool:
        return time() >= self.visual_time_min

    @callback(order=1)
    def update_sequential(self):
        elapsed = time() - self.visual_time_min

        if self.note_judgment != judge.MISS or elapsed < self.duration + judge.TAP_WINDOWS[judge.BAD]:
            self._draw_note(elapsed)

        if self.note_judgment == judge.MISS and elapsed - self.duration >= judge.TAP_WINDOWS[judge.BAD]:
            self._finalize(judge.MISS, 0.0)

    def _draw_note(self, elapsed: float):
        t = elapsed / self.duration
        screen_x, screen_y, screen_w, screen_h = layout.project(self.world_x, t, self.width_raw)
        quad = layout.note_quad(screen_x, screen_y, screen_w, screen_h)
        Skin.tap.draw(quad, z=-self.target_time)

    def _finalize(self, judgment: int, accuracy: float):
        self.note_judgment = judgment
        sonolus_judgment = judge.to_sonolus_judgment(judgment)
        self.result.judgment = sonolus_judgment
        self.result.accuracy = accuracy
        self.result.bucket = Buckets.tap
        self.result.bucket_value = accuracy
        self.result.haptic = HapticType.NONE if sonolus_judgment == Judgment.MISS else HapticType.LIGHT
        self.despawn = True

    @callback(order=2)
    def touch(self):
        if self.note_judgment != judge.MISS:
            return

        for t in touches():
            if not t.started:
                continue

            diff = time() - self.target_time
            j = judge.judge_tap(diff)

            if j != judge.MISS:
                self._finalize(j, diff)
                return


class FlickNote(PlayArchetype):
    name = "FlickNote"

    is_scored = True

    beat: float = imported(name="beat")
    l1_raw: float = imported(name="l1")
    r1_raw: float = imported(name="r1")

    visual_time_min: float = entity_memory()
    visual_time_max: float = entity_memory()

    target_time: float = entity_memory()
    duration: float = entity_memory()
    speed: float = entity_memory()
    middle_x: float = entity_memory()
    world_x: float = entity_memory()
    width_raw: float = entity_memory()

    note_judgment: int = entity_memory()

    tracked_touch_id: int = entity_memory()
    pending_judgment: int = entity_memory()
    pending_diff: float = entity_memory()
    is_tracking: bool = entity_memory()

    @callback(order=1)
    def preprocess(self):
        Buckets.flick.window = JudgmentWindow(
            perfect=Interval(-judge.FLICK_MIN_DIFF, judge.FLICK_MIN_DIFF),
            great=Interval(-judge.FLICK_MAX_DIFF, judge.FLICK_MAX_DIFF),
            good=Interval(-judge.FLICK_MAX_DIFF, judge.FLICK_MAX_DIFF),
        )
        self.target_time = self.beat
        self.speed = Options.speed
        self.duration = layout.solve_fall_duration(self.speed)
        self.visual_time_max = self.target_time
        self.visual_time_min = self.target_time - self.duration

        self.middle_x = layout.raw_to_middle_x(self.l1_raw, self.r1_raw)
        self.world_x = layout.get_world_x(self.middle_x)
        self.width_raw = self.r1_raw - self.l1_raw

        self.note_judgment = judge.MISS
        self.is_tracking = False
        self.tracked_touch_id = -1

    def spawn_order(self) -> float:
        return self.visual_time_min

    def should_spawn(self) -> bool:
        return time() >= self.visual_time_min

    @callback(order=1)
    def update_sequential(self):
        elapsed = time() - self.visual_time_min

        if self.note_judgment != judge.MISS or elapsed < self.duration + judge.FLICK_MAX_DIFF:
            self._draw_note(elapsed)

        if self.note_judgment == judge.MISS and elapsed - self.duration >= judge.FLICK_MAX_DIFF:
            self._finalize(judge.MISS, 0.0)

    def _draw_note(self, elapsed: float):
        t = elapsed / self.duration
        screen_x, screen_y, screen_w, screen_h = layout.project(self.world_x, t, self.width_raw)
        quad = layout.note_quad(screen_x, screen_y, screen_w, screen_h)
        Skin.flick.draw(quad, z=-self.target_time)

        bob = layout.flick_arrow_bob_offset(elapsed)
        arrow_quad = layout.flick_arrow_quad(screen_x, screen_y, screen_w, screen_h, bob)
        Skin.flick_arrow.draw(arrow_quad, z=-self.target_time - 0.001)

    def _finalize(self, judgment: int, accuracy: float):
        self.note_judgment = judgment
        sonolus_judgment = judge.to_sonolus_judgment(judgment)
        self.result.judgment = sonolus_judgment
        self.result.accuracy = accuracy
        self.result.bucket = Buckets.flick
        self.result.bucket_value = accuracy
        self.result.haptic = HapticType.NONE if sonolus_judgment == Judgment.MISS else HapticType.LIGHT
        self.despawn = True

    def _hitbox_contains(self, x: float, y: float) -> bool:
        elapsed = time() - self.visual_time_min
        t = elapsed / self.duration
        screen_x, screen_y, w, h = layout.project(self.world_x, t, self.width_raw)
        return (
            screen_x - w / 2 <= x <= screen_x + w / 2
            and screen_y - h / 2 <= y <= screen_y + h / 2
        )

    @callback(order=2)
    def touch(self):
        if self.note_judgment != judge.MISS:
            return

        if self.is_tracking:
            self._update_tracked_touch()
            return

        for t in touches():
            if not t.started:
                continue
            if not self._hitbox_contains(t.position.x, t.position.y):
                continue

            diff = time() - self.target_time
            j = judge.judge_flick(diff)

            if j == judge.MISS:
                continue

            self.tracked_touch_id = t.id
            self.pending_judgment = j
            self.pending_diff = diff
            self.is_tracking = True
            return

    def _update_tracked_touch(self):
        for t in touches():
            if t.id != self.tracked_touch_id:
                continue

            if t.ended:
                self.is_tracking = False
                return

            delta = t.total_delta
            dist_sq = delta.x * delta.x + delta.y * delta.y

            if dist_sq >= judge.FLICK_DISTANCE_NORMALIZED:
                self.is_tracking = False
                self._finalize(self.pending_judgment, self.pending_diff)
            return

        self.is_tracking = False


play_mode = PlayMode(
    archetypes=[Stage, TapNote, FlickNote],
    skin=Skin,
)