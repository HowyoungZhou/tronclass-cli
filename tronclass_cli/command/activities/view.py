from yaml import dump, CDumper as Dumper

from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.utils import nested_dict_select, iter_select_where


class ActivitiesViewCommand(Command):
    name = 'activities.view'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        self._parser.add_argument('course_id', help='course id')
        self._parser.add_argument('activity_id', help='activity id')
        default_fields = 'id,title,type,data,deadline,uploads'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        activities = self._ctx.api.get_activities(args.course_id)
        activity = iter_select_where(activities, lambda x: args.activity_id == str(x['id']))
        if activity:
            print(dump(nested_dict_select(activity, fields), Dumper=Dumper, allow_unicode=True, sort_keys=False))
        else:
            raise KeyError(f'activity {args.activity_id} not found in course {args.course_id}')
