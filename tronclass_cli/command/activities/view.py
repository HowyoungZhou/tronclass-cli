from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.middleware.table import TableMiddleware
from tronclass_cli.utils import unflatten_fields, nested_dict_select
from yaml import dump, CLoader as Loader, CDumper as Dumper


class ActivitiesViewCommand(Command):
    name = 'activities.view'
    middleware_classes = [ApiMiddleware, TableMiddleware]

    def _init_parser(self):
        self._parser.add_argument('course_id')
        self._parser.add_argument('activity_id')
        default_fields = 'id,title,type,data,deadline,uploads'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        activities = self._ctx.api.get_activities(args.course_id)
        for activity in activities:
            if args.activity_id == str(activity['id']):
                print(dump(nested_dict_select(activity, fields), Dumper=Dumper))
