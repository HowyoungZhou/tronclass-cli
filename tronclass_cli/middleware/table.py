import re

from dateutil.parser import isoparse
from tabulate import tabulate

from tronclass_cli.middleware import Middleware
from tronclass_cli.utils import flatten_dict, dict_select


class TableMiddleware(Middleware):
    name = 'table'

    def _init_parser(self):
        group = self._parser.add_argument_group(self.name)
        group.add_argument('--table-fmt', default='simple', help='table format')
        group.add_argument('--date-fmt', default='%c', help='date format')

    def _exec(self, args):
        date_regex = re.compile(r'\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d(\.\d+)?([+-][0-2]\d:[0-5]\d|Z)')

        def process_value(value):
            if isinstance(value, list):
                return ', '.join([str(x) for x in value])
            elif isinstance(value, str) and date_regex.search(value):
                return isoparse(value).astimezone().strftime(args.date_fmt)
            return value

        def process_dict(data, fields):
            data = flatten_dict(data)
            data = dict_select(data, fields)
            return {k: process_value(v) for k, v in data.items()}

        def print_table(data, fields):
            data = [process_dict(d, fields) for d in data]
            print(tabulate(data, headers='keys', tablefmt=args.table_fmt))

        self._ctx.print_table = print_table
