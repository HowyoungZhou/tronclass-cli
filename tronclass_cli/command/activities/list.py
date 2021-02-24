from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.middleware.table import TableMiddleware
from tronclass_cli.utils import unflatten_fields


class ActivitiesListCommand(Command):
    name = 'activities.list'
    middleware_classes = [ApiMiddleware, TableMiddleware]

    def _init_parser(self):
        self._parser.add_argument('course_id', help='course id')
        default_fields = 'id,title,type'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        activities = list(self._ctx.api.get_activities(args.course_id, fields=unflatten_fields(fields)))
        if len(activities) == 0:
            print('No activities.')
        else:
            self._ctx.print_table(activities, fields)
