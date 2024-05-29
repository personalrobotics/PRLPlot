from typing import Any, Dict


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