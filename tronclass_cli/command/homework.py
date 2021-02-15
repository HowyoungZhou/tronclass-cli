from tabulate import tabulate

from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.utils import dict_select


class HomeworkCommand(Command):
    name = 'courses'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        self._parser.add_argument('course_id')

    def _exec(self, args):
        homework = dict_select(self._ctx.api.get_homework(args.course_id), ['id', 'title', 'deadline'])
        if len(homework) == 0:
            print('No homework.')
        else:
            print(tabulate(homework, headers='keys'))
