from yaml import dump, CDumper as Dumper

from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware
from tronclass_cli.utils import nested_dict_select


class ActivitiesViewCommand(Command):
    name = 'activities.view'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        self._parser.add_argument('activity_id', help='activity id')
        default_fields = 'id,title,type,data,deadline,uploads'
        self._parser.add_argument('--fields', default=default_fields,
                                  help=f'fields to display, default fields: {default_fields}')

    def _exec(self, args):
        fields = args.fields.split(',')
        activity = self._ctx.api.get_activity(args.activity_id)
        print(dump(nested_dict_select(activity, fields), Dumper=Dumper, allow_unicode=True, sort_keys=False))
