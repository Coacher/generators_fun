import inspect
from functools import wraps


def make_header(text, width=80, filler='-'):
    if not len(text):
        return filler * width

    # Spaces around text
    width -= 2

    if len(text) >= width:
        return text

    start = filler * ((width - len(text)) // 2)
    end = filler * (width - len(text) - len(start))

    return ' '.join((start, text, end))


def example(func):
    @wraps(func)
    def wrapper():
        code, _ = inspect.getsourcelines(func)
        _dec, _def, *body = code

        print(make_header(func.__name__.upper()))

        print(inspect.cleandoc(''.join(body)))

        print(make_header('OUTPUT:'))

        retval = func()
        if retval is not None:
            print(retval)

        print(make_header(''), '\n')

    return wrapper
