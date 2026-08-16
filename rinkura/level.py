from sonolus.script.level import Level, LevelData

from rinkura.play.mode import TapNote
from rinkura.play.stage import Stage

level = Level(
    name="rinkura_level",
    title="Link! Like! Love Live! Level",
    bgm=None,
    data=LevelData(
        bgm_offset=0,
        entities=[
            Stage(),
            TapNote(beat=12, l1_raw=25, r1_raw=35),
            TapNote(beat=13, l1_raw=15, r1_raw=25),
            TapNote(beat=14, l1_raw=35, r1_raw=45),
            TapNote(beat=15, l1_raw=25, r1_raw=35),
        ],
    ),
)


def load_levels():
    yield level
