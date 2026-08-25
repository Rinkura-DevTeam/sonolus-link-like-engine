def bisect(array, key, value):
    lo, hi = 0, len(array)
    while lo < hi:
        mid = (lo + hi) // 2
        if array[mid][key] < value:
            lo = mid + 1
        else:
            hi = mid
    return lo


def integrate(integrals):
    x = y = s = 0.0
    out = []
    for integral in integrals:
        y += (integral['x'] - x) * s
        x = integral['x']
        s = integral['s']
        out.append({**integral, 'x': x, 'y': y, 's': s})
    return out


def find_integral(integrals, key, value):
    index = bisect(integrals, key, value)
    if index < len(integrals) and integrals[index][key] == value:
        return integrals[index]
    return integrals[index - 1]


def to_bpm_integral(o):
    return {'x': o['Time'], 'y': 0.0, 's': o['Bpm'] / 60.0}


def create_bpms(bpms):
    return integrate(sorted((to_bpm_integral(b) for b in bpms), key=lambda b: b['x']))


def beat_to_time(bpms, beat):
    i = find_integral(bpms, 'y', beat)
    return i['x'] + (beat - i['y']) / i['s']


def time_to_beat(bpms, time):
    i = find_integral(bpms, 'x', time)
    val = i['y'] + (time - i['x']) * i['s']
    return round(val * 64) / 64