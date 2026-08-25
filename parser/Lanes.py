LANE_PIVOT = 29.5


def scale_lane(raw: int, lane_scale: float = 1.0) -> float:
    return (raw - LANE_PIVOT) * lane_scale + LANE_PIVOT