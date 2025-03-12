import json
from pathlib import Path


class DotDict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[f"{key.upper()}"] = value

    def __getattr__(self, key):
        return self.get(key, None)


def load_config():
    base_dir = Path(__file__).resolve().parent.parent.parent
    with open(f'{base_dir}/etc/properties.json') as f:
        config = json.load(f)
        return DotDict(config)
