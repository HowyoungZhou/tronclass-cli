from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.middleware.table import TableMiddleware


class HomeworkListCommand(Command):
    name = 'courses.list'
    middleware_classes = [ApiMiddleware, TableMiddleware]

    def _init_parser(self):
        self._parser.add_argument('course_id', help='course id')
        default_fields = 'id,title,deadline,submitted,score'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        homework = list(self._ctx.api.get_homework(args.course_id))
        if len(homework) == 0:
            print('No homework.')
        else:
            self._ctx.print_table(homework, fields)
