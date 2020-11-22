import json
import os

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


default_root = Path.home() / '.tronclass'
config_path = Path(os.getenv('TRONCLASS_CLI_CONFIG_FILE') or default_root / 'config.json')

config_dict = {}
if config_path.exists():
    with open(config_path) as fs:
        config_dict = json.load(fs)
config = Config(config_dict)


def get_config(name: str, default=None, value_type: type = str, type_converter=None):
    if type_converter is None:
        type_converter = value_type

    res = config_dict.get(name) or os.getenv('TRONCLASS_CLI_' + name.upper(), default)
    if res is None:
        raise KeyError(f'Config item {name} is required but missing.')

    try:
        if isinstance(res, value_type):
            res = type_converter(res)
    except Exception:
        raise ValueError(f'Config item {name} should be {type.__name__}.')
    return res


sessions_dir = get_config('sessions_dir', default_root / 'sessions', Path)
provider = get_config('provider', 'zju')
