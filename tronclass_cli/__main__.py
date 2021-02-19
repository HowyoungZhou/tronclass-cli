from argparse import ArgumentParser

from tronclass_cli.command.root import RootCommand
from tronclass_cli.command.todo import TodoCommand
from tronclass_cli.command.courses import CoursesCommand
from tronclass_cli.command.homework import HomeworkCommand
from tronclass_cli.middleware import Context

parser = ArgumentParser()
root_command = RootCommand(parser, Context())
root_command.add_sub_command('todo', TodoCommand)
root_command.add_sub_command('courses', CoursesCommand)
root_command.add_sub_command('homework', HomeworkCommand)


def main():
    args = root_command.parse_args()
    args.__middleware.exec(args)
    args.__middleware.dispose()


if __name__ == '__main__':
    main()
