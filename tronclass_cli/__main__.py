from argparse import ArgumentParser

from tronclass_cli.command.root import RootCommand
from tronclass_cli.command.todo import TodoCommand

parser = ArgumentParser()
root_command = RootCommand(parser, [])
root_command.add_sub_command('todo', TodoCommand)

args = root_command.parser.parse_args()
args.__command.exec(args)
