from sonolus.script.archetype import PlayArchetype, callback
from sonolus.script.quad import Rect
from sonolus.script.vec import Vec2

from rinkura.lib import layout
from rinkura.lib.skin import Skin

CAP_WIDTH = 0.12
LINE_HEIGHT = 0.05


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
        half = layout.STAGE_HALF_WIDTH

        left_rect = Rect.from_center(
            center=Vec2(-half + CAP_WIDTH / 2, y),
            dimensions=Vec2(CAP_WIDTH, LINE_HEIGHT),
        )
        right_rect = Rect.from_center(
            center=Vec2(half - CAP_WIDTH / 2, y),
            dimensions=Vec2(CAP_WIDTH, LINE_HEIGHT),
        )
        center_rect = Rect.from_center(
            center=Vec2(0, y),
            dimensions=Vec2((half - CAP_WIDTH) * 2, LINE_HEIGHT),
        )

        Skin.judgment_line_left.draw(left_rect, z=10.0)
        Skin.judgment_line_right.draw(right_rect, z=10.0)
        Skin.judgment_line_center.draw(center_rect, z=10.0)
