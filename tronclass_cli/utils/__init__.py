def dict_select(dicts, keys):
    return [{k: d[k] for k in keys} for d in dicts]
