from argparse import ArgumentParser

from tronclass_cli.command.root import RootCommand
from tronclass_cli.command.todo import TodoCommand
from tronclass_cli.middleware import Context

parser = ArgumentParser()
root_command = RootCommand(parser, Context())
root_command.add_sub_command('todo', TodoCommand)

args = root_command.parse_args()
args.__middleware.exec(args)
