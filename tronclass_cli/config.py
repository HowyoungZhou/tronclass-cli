import json
import os

from pathlib import Path

default_root = Path.home() / '.tronclass'
config_path = Path(os.getenv('TRONCLASS_CLI_CONFIG_FILE') or default_root / 'config.json')

config_dict = {}
if config_path.exists():
    with open(config_path) as fs:
        config_dict = json.load(fs)


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
