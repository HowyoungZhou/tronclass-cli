import tronclass_cli
from tronclass_cli.command import Command


class RootCommand(Command):
    name = 'root'

    def _init_parser(self):
        self._parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + tronclass_cli.__version__)

    def _exec(self, args):
        self._parser.print_help()

    def parse_args(self, *args, **kwargs):
        return self._parser.parse_args(*args, **kwargs)
