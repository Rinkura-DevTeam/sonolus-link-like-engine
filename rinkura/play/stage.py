from sonolus.script.archetype import PlayArchetype, callback
from sonolus.script.quad import Rect
from sonolus.script.vec import Vec2

from rinkura.lib import layout
from rinkura.lib.skin import Skin

LINE_HEIGHT = 0.24


class Stage(PlayArchetype):
    name = "Stage"

    is_scored = False

    @callback(order=1)
    def preprocess(self):
        pass

    def spawn_order(self) -> float:
        return -1e8

    def should_spawn(self) -> bool:
        return True

    @callback(order=0)
    def update_sequential(self):
        y = layout.JUDGE_LINE_Y
        half = layout.stage_half_width()
        cap_width = half * 0.12

        left_rect = Rect.from_center(
            center=Vec2(-half - cap_width / 2, y),
            dimensions=Vec2(cap_width, LINE_HEIGHT),
        )
        right_rect = Rect.from_center(
            center=Vec2(half + cap_width / 2, y),
            dimensions=Vec2(cap_width, LINE_HEIGHT),
        )
        center_rect = Rect.from_center(
            center=Vec2(0, y),
            dimensions=Vec2(half * 2, LINE_HEIGHT),
        )

        Skin.judgment_line_left.draw(left_rect, z=10.0)
        Skin.judgment_line_right.draw(right_rect, z=10.0)
        Skin.judgment_line_center.draw(center_rect, z=10.0)

        Skin.stage.draw(layout.stage_quad(), z=5.0)