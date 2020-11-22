import json

from pathlib import Path


class Config:
    def __init__(self, data: dict):
        self._data = data

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def get_section(self, name):
        return Config(self._data.get(name, {}))

    def get(self, name: str, default=None, required=False, value_type: type = None, type_converter=None):
        res = self._data.get(name, default)
        if required and res is None:
            raise KeyError(f'Config item {name} is required but missing.')
        if value_type is not None:
            try:
                if not isinstance(res, value_type):
                    res = type_converter(res)
            except Exception:
                raise ValueError(f'Config item {name} should be {type.__name__}.')
        return res

    def to_dict(self):
        return self._data


def load_config(path):
    path = Path(path)
    config_dict = {}
    if path.exists():
        with open(path) as fs:
            config_dict = json.load(fs)
    return Config(config_dict)
