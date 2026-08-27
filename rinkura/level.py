from pathlib import Path

from sonolus.script.level import Level, LevelData

from rinkura.lib.chart_loader import load_level_data
from rinkura.lib.leveldata_loader import load_exported_level_data
from rinkura.play.mode import FlickNote, HoldEndNote, HoldHeadNote, HoldTickNote, TapNote, TraceNote
from rinkura.play.stage import Stage

CHARTS_DIR = Path(__file__).parent.parent / "charts"
LEVELDATA_DIR = Path(__file__).parent.parent / "leveldata"

test_level = Level(
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
            TraceNote(beat=12, l1_raw=25, r1_raw=35),
            TraceNote(beat=13, l1_raw=15, r1_raw=25),
            HoldHeadNote(beat=14, end_beat=17, l1_raw=25, r1_raw=35, end_l1_raw=5, end_r1_raw=15),
            HoldTickNote(
                beat=14.5,
                head_beat=14, head_l1_raw=25, head_r1_raw=35,
                end_beat=17, end_l1_raw=5, end_r1_raw=15,
            ),
            HoldTickNote(
                beat=15,
                head_beat=14, head_l1_raw=25, head_r1_raw=35,
                end_beat=17, end_l1_raw=5, end_r1_raw=15,
            ),
            HoldTickNote(
                beat=15.5,
                head_beat=14, head_l1_raw=25, head_r1_raw=35,
                end_beat=17, end_l1_raw=5, end_r1_raw=15,
            ),
            HoldTickNote(
                beat=16,
                head_beat=14, head_l1_raw=25, head_r1_raw=35,
                end_beat=17, end_l1_raw=5, end_r1_raw=15,
            ),
            HoldTickNote(
                beat=16.5,
                head_beat=14, head_l1_raw=25, head_r1_raw=35,
                end_beat=17, end_l1_raw=5, end_r1_raw=15,
            ),
            HoldEndNote(beat=17, l1_raw=5, r1_raw=15),
        ],
    ),
)


def load_levels():
    yield test_level

    if CHARTS_DIR.exists():
        for chart_path in sorted(CHARTS_DIR.glob("*.json")):
            yield Level(
                name=chart_path.stem,
                title=chart_path.stem,
                bgm=None,
                data=load_level_data(str(chart_path)),
            )

    if LEVELDATA_DIR.exists():
        for leveldata_path in sorted(LEVELDATA_DIR.glob("*.gz")):
            yield Level(
                name=leveldata_path.stem.removesuffix(".json"),
                title=leveldata_path.stem.removesuffix(".json"),
                bgm=None,
                data=load_exported_level_data(str(leveldata_path)),
            )