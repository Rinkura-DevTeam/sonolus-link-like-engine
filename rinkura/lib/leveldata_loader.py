import gzip
import json
from pathlib import Path

from sonolus.script.level import BpmChange, LevelData

from rinkura.play.mode import (
    FlickNote,
    HoldEndNote,
    HoldHeadNote,
    HoldTickNote,
    TapNote,
    TraceNote,
)
from rinkura.play.stage import Stage

ARCHETYPE_BUILDERS = {
    "Stage": lambda data: Stage(),
    "TapNote": lambda data: TapNote(beat=data["beat"], l1_raw=data["l1"], r1_raw=data["r1"]),
    "FlickNote": lambda data: FlickNote(beat=data["beat"], l1_raw=data["l1"], r1_raw=data["r1"]),
    "TraceNote": lambda data: TraceNote(beat=data["beat"], l1_raw=data["l1"], r1_raw=data["r1"]),
    "HoldHeadNote": lambda data: HoldHeadNote(
        beat=data["beat"], end_beat=data["end_beat"],
        l1_raw=data["l1"], r1_raw=data["r1"],
        end_l1_raw=data["end_l1"], end_r1_raw=data["end_r1"],
    ),
    "HoldTickNote": lambda data: HoldTickNote(
        beat=data["beat"],
        head_beat=data["head_beat"], head_l1_raw=data["head_l1"], head_r1_raw=data["head_r1"],
        end_beat=data["end_beat"], end_l1_raw=data["end_l1"], end_r1_raw=data["end_r1"],
    ),
    "HoldEndNote": lambda data: HoldEndNote(beat=data["beat"], l1_raw=data["l1"], r1_raw=data["r1"]),
    "#BPM_CHANGE": lambda data: BpmChange(beat=data["#BEAT"], bpm=data["#BPM"]),
}


def load_exported_level_data(path: str) -> LevelData:
    raw_bytes = Path(path).read_bytes()

    if raw_bytes[:2] == b"\x1f\x8b":
        raw_bytes = gzip.decompress(raw_bytes)

    raw = json.loads(raw_bytes.decode("utf-8"))

    entities = []
    for entity in raw["entities"]:
        archetype = entity["archetype"]
        builder = ARCHETYPE_BUILDERS.get(archetype)
        if builder is None:
            continue

        data = {item["name"]: item["value"] for item in entity["data"] if "value" in item}
        entities.append(builder(data))

    return LevelData(bgm_offset=raw["bgmOffset"], entities=entities)