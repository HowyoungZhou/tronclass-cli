from tabulate import tabulate

from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware


class TodoCommand(Command):
    name = 'todo'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        pass

    def _exec(self, args):
        todo = list(self._ctx.api.get_todo())
        if len(todo) == 0:
            print('No tasks.')
        else:
            print(tabulate(todo, headers='keys'))
