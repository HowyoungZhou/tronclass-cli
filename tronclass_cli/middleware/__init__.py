from argparse import ArgumentParser


class Middleware:
    def __init__(self):
        self.parser = ArgumentParser(add_help=False)
        self.init_parser()

    def init_parser(self):
        pass

    def exec(self, args, ctx):
        pass
