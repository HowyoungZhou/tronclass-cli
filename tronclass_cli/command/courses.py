from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.middleware.console import ConsoleMiddleware
from tronclass_cli.middleware.table import TableMiddleware
from tronclass_cli.utils import unflatten_fields


class CoursesCommand(Command):
    name = 'courses'

    def _exec(self, args):
        self._parser.print_help()


class CoursesListCommand(Command):
    name = 'courses.list'
    middleware_classes = [ApiMiddleware, TableMiddleware, ConsoleMiddleware]

    def _init_parser(self):
        default_fields = 'id,name,instructors.name'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        with self._ctx.console.status("Fetching courses list..."):
            courses = list(self._ctx.api.get_courses(fields=unflatten_fields(fields)))
        if len(courses) == 0:
            print('No courses.')
        else:
            self._ctx.print_table(courses, fields)
