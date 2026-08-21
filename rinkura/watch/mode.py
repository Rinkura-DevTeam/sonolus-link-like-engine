from sonolus.script.archetype import (
    StandardImport,
    WatchArchetype,
    callback,
    entity_memory,
    imported,
)
from sonolus.script.bucket import Judgment
from sonolus.script.engine import WatchMode
from sonolus.script.runtime import is_replay, time

from rinkura.lib import layout
from rinkura.lib.buckets import Buckets
from rinkura.lib.effect import Effects
from rinkura.lib.options import Options
from rinkura.lib.particle import Particles
from rinkura.lib.skin import Skin
from rinkura.watch.update_spawn import update_spawn


class TapNote(WatchArchetype):
    name = "TapNote"

    is_scored = True

    beat: float = imported(name="beat")
    l1_raw: float = imported(name="l1")
    r1_raw: float = imported(name="r1")

    judgment: StandardImport.JUDGMENT
    accuracy: StandardImport.ACCURACY

    target_time: float = entity_memory()
    duration: float = entity_memory()
    speed: float = entity_memory()
    middle_x: float = entity_memory()
    world_x: float = entity_memory()
    width_raw: float = entity_memory()
    resolved_judgment: Judgment = entity_memory()

    hit: bool = entity_memory()

    @callback(order=1)
    def preprocess(self):
        self.target_time = self.beat
        self.speed = Options.speed
        self.duration = layout.solve_fall_duration(self.speed)

        self.middle_x = layout.raw_to_middle_x(self.l1_raw, self.r1_raw)
        self.world_x = layout.get_world_x(self.middle_x)
        self.width_raw = self.r1_raw - self.l1_raw

        if is_replay():
            self.resolved_judgment = self.judgment
        else:
            self.resolved_judgment = Judgment.PERFECT

        self.result.target_time = self.target_time
        self.result.bucket = Buckets.tap
        self.result.bucket_value = self.accuracy * 1000 if is_replay() else 0.0

        self.hit = False

    def spawn_time(self) -> float:
        return self.target_time - self.duration

    def despawn_time(self) -> float:
        return self.target_time + 0.1

    @callback(order=1)
    def update_sequential(self):
        elapsed = time() - (self.target_time - self.duration)

        if not self.hit and time() >= self.target_time:
            self._trigger_hit()

        if not self.hit:
            self._draw_note(elapsed)

    def _draw_note(self, elapsed: float):
        t = elapsed / self.duration
        screen_x, screen_y, screen_w, screen_h = layout.project(self.world_x, t, self.width_raw)
        quad = layout.note_quad(screen_x, screen_y, screen_w, screen_h)
        Skin.tap.draw(quad, z=-self.target_time)

    def _trigger_hit(self):
        self.hit = True

        if self.resolved_judgment == Judgment.MISS:
            return

        screen_x, screen_y, screen_w, screen_h = layout.project(self.world_x, 1.0, self.width_raw)
        quad = layout.note_quad(screen_x, screen_y, screen_w, screen_h)
        Particles.note.spawn(quad, duration=0.2)
        Effects.perfect.play()


class FlickNote(WatchArchetype):
    name = "FlickNote"

    is_scored = True

    beat: float = imported(name="beat")
    l1_raw: float = imported(name="l1")
    r1_raw: float = imported(name="r1")

    judgment: StandardImport.JUDGMENT
    accuracy: StandardImport.ACCURACY

    target_time: float = entity_memory()
    duration: float = entity_memory()
    speed: float = entity_memory()
    middle_x: float = entity_memory()
    world_x: float = entity_memory()
    width_raw: float = entity_memory()
    resolved_judgment: Judgment = entity_memory()

    hit: bool = entity_memory()

    @callback(order=1)
    def preprocess(self):
        self.target_time = self.beat
        self.speed = Options.speed
        self.duration = layout.solve_fall_duration(self.speed)

        self.middle_x = layout.raw_to_middle_x(self.l1_raw, self.r1_raw)
        self.world_x = layout.get_world_x(self.middle_x)
        self.width_raw = self.r1_raw - self.l1_raw

        if is_replay():
            self.resolved_judgment = self.judgment
        else:
            self.resolved_judgment = Judgment.PERFECT

        self.result.target_time = self.target_time
        self.result.bucket = Buckets.flick
        self.result.bucket_value = self.accuracy * 1000 if is_replay() else 0.0

        self.hit = False

    def spawn_time(self) -> float:
        return self.target_time - self.duration

    def despawn_time(self) -> float:
        return self.target_time + 0.1

    @callback(order=1)
    def update_sequential(self):
        elapsed = time() - (self.target_time - self.duration)

        if not self.hit and time() >= self.target_time:
            self._trigger_hit()

        if not self.hit:
            self._draw_note(elapsed)

    def _draw_note(self, elapsed: float):
        t = elapsed / self.duration
        screen_x, screen_y, screen_w, screen_h = layout.project(self.world_x, t, self.width_raw)
        quad = layout.note_quad(screen_x, screen_y, screen_w, screen_h)
        Skin.flick.draw(quad, z=-self.target_time)

        arrow_quad = layout.flick_arrow_quad(screen_x, screen_y, screen_w, screen_h)
        Skin.flick_arrow.draw(arrow_quad, z=-self.target_time - 0.001)

    def _trigger_hit(self):
        self.hit = True

        if self.resolved_judgment == Judgment.MISS:
            return

        screen_x, screen_y, screen_w, screen_h = layout.project(self.world_x, 1.0, self.width_raw)
        quad = layout.note_quad(screen_x, screen_y, screen_w, screen_h)
        Particles.note.spawn(quad, duration=0.2)
        Effects.perfect.play()


watch_mode = WatchMode(
    archetypes=[TapNote, FlickNote],
    skin=Skin,
    effects=Effects,
    particles=Particles,
    buckets=Buckets,
    update_spawn=update_spawn,
)
