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
        self.speed = 1.0
        self.duration = layout.solve_fall_duration(self.speed)
        self.visual_time_max = self.target_time
        self.visual_time_min = self.target_time - self.duration
        self.n_offset = 0.0

        self.middle_x = layout.raw_to_middle_x(self.l1_raw, self.r1_raw)
        self.world_x = layout.get_world_x(self.middle_x)

        self.note_judgment = judge.MISS

    def spawn_order(self) -> float:
        return self.visual_time_min

    def should_spawn(self) -> bool:
        return time() >= self.visual_time_min

    @callback(order=1)
    def update_sequential(self):
        elapsed = time() - self.visual_time_min
        world_z = layout.get_world_z(elapsed, self.duration, self.speed, self.n_offset)

        if self.note_judgment != judge.MISS or elapsed < self.duration:
            self._draw_note(world_z)

        if self.note_judgment == judge.MISS and elapsed - self.duration >= judge.TAP_WINDOWS[judge.BAD]:
            self._finalize(judge.MISS, 0.0)

    def _draw_note(self, world_z: float):
        screen_x, screen_y, size = layout.project(self.world_x, world_z)
        quad = layout.note_quad(screen_x, screen_y, size)
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


play_mode = PlayMode(
    archetypes=[Stage, TapNote],
    skin=Skin,
)
