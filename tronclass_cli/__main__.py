from argparse import ArgumentParser

from tronclass_cli.command.activities.view import ActivitiesViewCommand
from tronclass_cli.command.cache import CacheCommand, CacheClearCommand
from tronclass_cli.command.root import RootCommand
from tronclass_cli.command.todo import TodoCommand
from tronclass_cli.command.courses import CoursesCommand, CoursesListCommand
from tronclass_cli.command.homework import HomeworkCommand, HomeworkListCommand, HomeworkSubmitCommand
from tronclass_cli.command.activities import ActivitiesCommand, ActivitiesListCommand, ActivitiesDownloadCommand
from tronclass_cli.middleware import Context
from tronclass_cli.utils import interact

parser = ArgumentParser()
root_command = RootCommand(parser, Context())
root_command.add_sub_command('todo', TodoCommand, aliases=['t', 'td'], help='view to-do list')

courses_command = root_command.add_sub_command('courses', CoursesCommand, aliases=['c'], help='manage all courses')
courses_command.add_sub_command('list', CoursesListCommand, aliases=['l', 'ls'], help='list courses')

activities_command = root_command.add_sub_command('activities', ActivitiesCommand, aliases=['a'],
                                                  help='manage activities of the courses')
activities_command.add_sub_command('list', ActivitiesListCommand, aliases=['l', 'ls'], help='list activities')
activities_command.add_sub_command('view', ActivitiesViewCommand, aliases=['v'], help='view an activity')
activities_command.add_sub_command('download', ActivitiesDownloadCommand, aliases=['d', 'dl'],
                                   help='download attached files')

homework_command = root_command.add_sub_command('homework', HomeworkCommand, aliases=['h', 'hw'],
                                                help='manage homework of the courses')
homework_command.add_sub_command('list', HomeworkListCommand, aliases=['l', 'ls'], help='list homework')
homework_command.add_sub_command('submit', HomeworkSubmitCommand, aliases=['s'], help='submit homework')

cache_command = root_command.add_sub_command('cache', CacheCommand, help='manage the cache data')
cache_command.add_sub_command('clear', CacheClearCommand, help='clear the cache data')


def main():
    args = root_command.parse_args()
    try:
        args.__middleware.exec(args)
        args.__middleware.dispose()
    except Exception as ex:
        interact.error(f'fatal: {ex}')


if __name__ == '__main__':
    main()
