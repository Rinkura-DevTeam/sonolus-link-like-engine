from sonolus.script.archetype import (
    PlayArchetype,
    callback,
    entity_memory,
    imported,
)
from sonolus.script.runtime import time, touches

from rinkura.lib import judge, layout
from rinkura.lib.options import Options
from rinkura.lib.skin import Skin


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

    note_judgment: int = entity_memory()

    @callback(order=1)
    def preprocess(self):
        self.target_time = self.beat
        self.speed = Options.speed
        self.duration = layout.solve_fall_duration(self.speed)
        self.visual_time_max = self.target_time
        self.visual_time_min = self.target_time - self.duration

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
        t = elapsed / self.duration

        if self.note_judgment != judge.MISS or elapsed < self.duration + judge.TAP_WINDOWS[judge.BAD]:
            self._draw_note(t)

        if self.note_judgment == judge.MISS and elapsed - self.duration >= judge.TAP_WINDOWS[judge.BAD]:
            self._finalize(judge.MISS)

    def _draw_note(self, t: float):
        screen_x, screen_y, w, h = layout.project(self.world_x, t, self.width_raw)
        quad = layout.note_quad(screen_x, screen_y, w, h)
        Skin.tap.draw(quad, z=-self.target_time)

    def _finalize(self, judgment: int):
        self.note_judgment = judgment
        self.result.judgment = judge.to_sonolus_judgment(judgment)
        self.result.accuracy = 0.0
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
                self._finalize(j)
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
    tracked_start_x: float = entity_memory()
    tracked_start_y: float = entity_memory()
    tracked_start_time: float = entity_memory()
    is_tracking: bool = entity_memory()

    @callback(order=1)
    def preprocess(self):
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
        t = elapsed / self.duration

        if self.note_judgment != judge.MISS or elapsed < self.duration + judge.FLICK_MAX_DIFF:
            self._draw_note(t, elapsed)

        if self.note_judgment == judge.MISS and elapsed - self.duration >= judge.FLICK_MAX_DIFF:
            self._finalize(judge.MISS)

    def _draw_note(self, t: float, elapsed: float):
        screen_x, screen_y, w, h = layout.project(self.world_x, t, self.width_raw)
        quad = layout.note_quad(screen_x, screen_y, w, h)
        Skin.flick.draw(quad, z=-self.target_time)

        bob = layout.flick_arrow_bob_offset(elapsed)
        arrow_quad = layout.flick_arrow_quad(screen_x, screen_y, w, h, bob)
        Skin.flick_arrow.draw(arrow_quad, z=-self.target_time - 0.001)

    def _finalize(self, judgment: int):
        self.note_judgment = judgment
        self.result.judgment = judge.to_sonolus_judgment(judgment)
        self.result.accuracy = 0.0
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
            if not self._hitbox_contains(t.x, t.y):
                continue

            self.tracked_touch_id = t.id
            self.tracked_start_x = t.x
            self.tracked_start_y = t.y
            self.tracked_start_time = time()
            self.is_tracking = True
            return

    def _update_tracked_touch(self):
        for t in touches():
            if t.id != self.tracked_touch_id:
                continue

            if t.ended:
                self.is_tracking = False
                self._evaluate_flick(t.x, t.y)
                return

            self._evaluate_flick(t.x, t.y)
            return

        self.is_tracking = False

    def _evaluate_flick(self, current_x: float, current_y: float):
        dx = current_x - self.tracked_start_x
        dy = current_y - self.tracked_start_y
        dist_sq = dx * dx + dy * dy
        dt = time() - self.tracked_start_time

        if dist_sq < judge.FLICK_DISTANCE:
            return
        if dt > judge.FLICK_VALID_TIME:
            self.is_tracking = False
            return

        diff = time() - self.target_time
        j = judge.judge_flick(diff)

        if j != judge.MISS:
            self.is_tracking = False
            self._finalize(j)


from sonolus.script.engine import PlayMode

play_mode = PlayMode(
    archetypes=[TapNote, FlickNote],
    skin=Skin,
)