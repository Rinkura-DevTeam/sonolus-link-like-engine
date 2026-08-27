from parser import Chart, NoteType, create_bpms, parse_chart, time_to_beat

from sonolus.script.level import BpmChange, LevelData

from rinkura.play.mode import FlickNote, HoldEndNote, HoldHeadNote, HoldTickNote, TapNote, TraceNote
from rinkura.play.stage import Stage


def build_level_data(chart: Chart) -> LevelData:
    bpms = create_bpms([{"Bpm": b.bpm, "Time": b.time} for b in chart.bpms])

    entities = [Stage()]

    for bpm_point in chart.bpms:
        entities.append(
            BpmChange(
                beat=time_to_beat(bpms, bpm_point.time),
                bpm=bpm_point.bpm,
            )
        )

    for note in chart.notes:
        beat = time_to_beat(bpms, note.just)
        l1_raw = note.flags.l1_raw
        r1_raw = note.flags.r1_raw

        match note.type:
            case NoteType.Single:
                entities.append(TapNote(beat=beat, l1_raw=l1_raw, r1_raw=r1_raw))
            case NoteType.Flick:
                entities.append(FlickNote(beat=beat, l1_raw=l1_raw, r1_raw=r1_raw))
            case NoteType.Trace:
                entities.append(TraceNote(beat=beat, l1_raw=l1_raw, r1_raw=r1_raw))
            case NoteType.Hold:
                if not note.holds:
                    continue

                tick_beats = [time_to_beat(bpms, h) for h in note.holds]
                end_beat = tick_beats[-1]
                l2_raw = note.flags.l2_raw
                r2_raw = note.flags.r2_raw

                entities.append(
                    HoldHeadNote(
                        beat=beat, end_beat=end_beat,
                        l1_raw=l1_raw, r1_raw=r1_raw,
                        end_l1_raw=l2_raw, end_r1_raw=r2_raw,
                    )
                )
                for tick_beat in tick_beats[:-1]:
                    entities.append(
                        HoldTickNote(
                            beat=tick_beat,
                            head_beat=beat, head_l1_raw=l1_raw, head_r1_raw=r1_raw,
                            end_beat=end_beat, end_l1_raw=l2_raw, end_r1_raw=r2_raw,
                        )
                    )
                entities.append(
                    HoldEndNote(beat=end_beat, l1_raw=l2_raw, r1_raw=r2_raw)
                )

    return LevelData(bgm_offset=chart.offset, entities=entities)


def load_level_data(path: str) -> LevelData:
    return build_level_data(parse_chart(path))