from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.middleware.table import TableMiddleware


class TodoCommand(Command):
    name = 'todo'
    middleware_classes = [ApiMiddleware, TableMiddleware]

    def _init_parser(self):
        default_fields = 'course_id,course_name,end_time,id,title,type'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        todo = list(self._ctx.api.get_todo())
        if len(todo) == 0:
            print('No courses.')
        else:
            self._ctx.print_table(todo, fields)
