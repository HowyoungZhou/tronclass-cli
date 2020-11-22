import sys


def prompt(text: str):
    print(text)


def prompt_input(prompt: str, default: str = None):
    if default is not None:
        prompt += f' [{default}]'
    prompt += ': '
    res = input(prompt)
    if res == '':
        res = default
    return res


def error(prompt):
    print(prompt, file=sys.stderr)


def select(prompt: str, options):
    print(prompt)
    for i, option in enumerate(options):
        print(f'[{i}] {option}')
    while True:
        try:
            i = int(input(f'[0-{len(options) - 1}]: '))
            if i < 0 or i >= len(options):
                raise ValueError()
            return i
        except ValueError:
            error(f'Please input an integer between 0 and {len(options) - 1}.')
            continue
