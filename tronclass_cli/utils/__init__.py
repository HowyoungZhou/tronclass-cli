from dateutil.parser import isoparse


def iter_select_where(iter, predicate):
    for it in iter:
        if predicate(it):
            return it
    return None


def dict_select(dict, keys):
    return {k: dict.get(k) for k in keys}


def nested_dict_select(dict, keys):
    res = {}
    for key in keys:
        dst = res
        src = dict
        *layers, last = key.split('.')
        for k in layers:
            dst = dst.setdefault(k, {})
            src = src.setdefault(k, {})
        dst[last] = src.get(last)
    return res


def flatten_dict(d, separator='.'):
    out = {}
    for key, val in d.items():
        if isinstance(val, dict):
            val = [val]
        if isinstance(val, list):
            for child in val:
                if isinstance(child, dict):
                    deeper = flatten_dict(child)
                    for key2, val2 in deeper.items():
                        out.setdefault(key + separator + key2, []).append(val2)
                else:
                    out.setdefault(key, []).append(child)
        else:
            out[key] = val
    return out


def process_table_data(data, key_filter):
    data = flatten_dict(data)
    data = dict_select(data, key_filter)

    def process_value(value):
        if isinstance(value, list):
            return ', '.join([str(x) for x in value])
        try:
            date = isoparse(value)
            return date.astimezone().strftime('%c')
        except:
            return value
        return value

    return {k: process_value(v) for k, v in data.items()}


def unflatten_fields(flatten_fields):
    fields = {}
    for field in flatten_fields:
        cur = fields
        for layer in field.split('.'):
            cur = cur.setdefault(layer, {})

    def visit(d):
        return ','.join([k if len(v) == 0 else f'{k}({visit(v)})' for k, v in d.items()])

    return visit(fields)
