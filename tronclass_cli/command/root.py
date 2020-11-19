import tronclass_cli
from tronclass_cli.command import Command


class RootCommand(Command):
    def init_parser(self):
        super(RootCommand, self).init_parser()
        self.parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + tronclass_cli.__version__)

    def exec(self, args):
        self.parser.print_help()
