from sonolus.script.level import Level, LevelData

from rinkura.play.mode import FlickNote, TapNote
from rinkura.play.stage import Stage

level = Level(
    name="test_level",
    title="Test Level",
    bgm=None,
    data=LevelData(
        bgm_offset=0,
        entities=[
            Stage(),
            TapNote(beat=6, l1_raw=25, r1_raw=35),
            TapNote(beat=7, l1_raw=15, r1_raw=25),
            TapNote(beat=8, l1_raw=35, r1_raw=45),
            TapNote(beat=9, l1_raw=25, r1_raw=35),
            FlickNote(beat=10, l1_raw=25, r1_raw=35),
            FlickNote(beat=11, l1_raw=15, r1_raw=25),
        ],
    ),
)


def load_levels():
    yield level