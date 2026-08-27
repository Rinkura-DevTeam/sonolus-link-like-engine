from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from .Lanes import scale_lane


class NoteType(IntEnum):
    Single = 0
    Hold = 1
    Flick = 2
    Trace = 3


@dataclass
class NoteFlags:
    type: NoteType
    r1_raw: int
    r2_raw: int
    l1_raw: int
    l2_raw: int
    is_mirror: bool = False
    lane_scale: float = 1.0

    @classmethod
    def from_ulong(cls, flags: int, is_mirror: bool = False, lane_scale: float = 1.0) -> "NoteFlags":
        return cls(
            type=NoteType(flags & 0xF),
            r1_raw=(flags >> 4) & 0x3F,
            r2_raw=(flags >> 10) & 0x3F,
            l1_raw=(flags >> 16) & 0x3F,
            l2_raw=(flags >> 22) & 0x3F,
            is_mirror=is_mirror,
            lane_scale=lane_scale,
        )

    @property
    def r1(self) -> float:
        return scale_lane(self.r1_raw, self.lane_scale)

    @property
    def r2(self) -> float:
        return scale_lane(self.r2_raw, self.lane_scale)

    @property
    def l1(self) -> float:
        return scale_lane(self.l1_raw, self.lane_scale)

    @property
    def l2(self) -> float:
        return scale_lane(self.l2_raw, self.lane_scale)

    @property
    def is_curve(self) -> bool:
        return self.l1_raw != self.l2_raw or self.r1_raw != self.r2_raw


@dataclass
class Note:
    uid: int
    just: float
    holds: list[float]
    flags: NoteFlags

    @property
    def type(self) -> NoteType:
        return self.flags.type


@dataclass
class BpmPoint:
    bpm: float
    time: float


@dataclass
class BeatPoint:
    numerator: int
    denominator: int
    time: float


@dataclass
class Chart:
    offset: float
    bpms: list[BpmPoint]
    beats: list[BeatPoint]
    notes: list[Note]