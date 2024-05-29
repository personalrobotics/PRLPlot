from typing import Any, Dict
import colorsys


def collapse_dict(d: Dict[str, Any], keys=None) -> Dict[str, Any]:
    if keys is None:
        keys = []
    new_d = {}
    for k, v in d.items():
        keys.append(k)
        if isinstance(v, dict):
            new_d.update(collapse_dict(v, keys))
        else:
            new_d[".".join(keys)] = v
        keys.pop()
    return new_d


def generate_baseline_color(idx: int, n_baselines: int):
    assert 0 <= idx < n_baselines, "Specified baseline index is out of the allowed range!"
    hue = (30 + 270 * idx / (n_baselines - 1)) / 360
    return colorsys.hls_to_rgb(hue, 0.85, 1.0)
