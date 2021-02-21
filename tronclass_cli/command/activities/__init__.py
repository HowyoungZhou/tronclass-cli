from tronclass_cli.command import Command

from .list import ActivitiesListCommand


class ActivitiesCommand(Command):
    name = 'activities'

    def _exec(self, args):
        self._parser.print_help()
