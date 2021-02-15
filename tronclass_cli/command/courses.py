from tabulate import tabulate

from tronclass_cli.command import Command
from tronclass_cli.middleware.api import ApiMiddleware


class CoursesCommand(Command):
    name = 'courses'
    middleware_classes = [ApiMiddleware]

    def _init_parser(self):
        pass

    def _exec(self, args):
        courses = list(self._ctx.api.get_courses())
        if len(courses) == 0:
            print('No courses.')
        else:
            courses = [{k: course[k] for k in ['id', 'name']} for course in courses]
            print(tabulate(courses, headers='keys'))
