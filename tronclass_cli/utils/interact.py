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
