from tronclass_cli.command import Command

from .list import HomeworkListCommand


class HomeworkCommand(Command):
    name = 'courses'

    def _exec(self, args):
        self._parser.print_help()
