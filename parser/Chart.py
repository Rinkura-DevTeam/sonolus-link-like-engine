import json

from .Types import BeatPoint, BpmPoint, Chart, Note, NoteFlags


def parse_chart(path: str) -> Chart:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    notes = []
    for n in raw["Notes"]:
        flags = NoteFlags.from_ulong(n["Flags"])
        notes.append(Note(
            uid=n["Uid"],
            just=float(n["just"]),
            holds=[float(h) for h in n["holds"]],
            flags=flags,
        ))

    bpms = [BpmPoint(b["Bpm"], b["Time"]) for b in raw["Bpms"]]
    beats = [BeatPoint(b["Numerator"], b["Denominator"], b["Time"]) for b in raw["Beats"]]

    return Chart(offset=raw["Offset"], bpms=bpms, beats=beats, notes=notes)
