# Generator methods: send (PEP-342)
# Описание:
#   https://docs.python.org/3/reference/expressions.html#generator.send
from traceback import print_exception

from common import example


@example
def example_1():
    """
    Генераторы имеют специальный метод send, который позволяет передавать
    извне данные внутрь генератора во время выполнения его кода.

    Вызов метода send передает его аргумент в левую часть текущего yield
    выражения, затем продолжает выполнение тела генератора до следующего
    yield или выхода из тела генератора, как обычно.

    Для передачи данных внутрь генератора он должен иметь текущую сохраненную
    точку выполнения в виде активного yield выражения, поэтому требуется хотя
    бы один раз вызвать метод __next__ перед использованием метода send.
    """
    def printer():
        lineno = 1
        while True:
            value = yield
            print(f'{lineno}:\t{value}')
            lineno += 1

    generator = printer()
    next(generator)

    generator.send('Hello there!')
    generator.send('Testing.. 1.. 2.. 3..')
    generator.send('Please stop!')

    generator.close()


example_1()


@example
def example_2():
    """
    Попытка использовать send до начала итерации по генератору приводит
    к ошибке, кроме единственного случая. PEP-342 гарантирует, что вызов
    send(None) эквивалентен вызову метода __next__.
    """

    def printer():
        lineno = 1
        while True:
            value = yield
            print(f'{lineno}:\t{value}')
            lineno += 1

    try:
        generator = printer()
        for c in 'VERTICAL':
            generator.send(c)
    except BaseException as err:
        print_exception(err)

    generator = printer()
    for c in [None] + list('VERTICAL'):
        generator.send(c)


example_2()


@example
def example_3():
    """
    Метод send возвращает значение, как если был бы вызван метод __next__.
    """
    def backwards():
        backwards = 'Give me a string!'
        while True:
            original = yield backwards
            print(f'Old backwards={backwards!r}, original={original!r}')
            backwards = original[::-1]
            print(f'New backwards={backwards!r}, original={original!r}')

    generator = backwards()
    print('Send None:')
    print(generator.send(None))
    print('Send First:')
    print(generator.send('First'))
    print('Send Second:')
    print(generator.send('Second'))
    print('Send Third:')
    print(generator.send('Third'))


example_3()


@example
def example_coroutine():
    """
    Чтобы каждый раз не вызывать метод __next__, удобно использовать декоратор.
    """
    def coroutine(func):
        def wrapper(*args, **kwargs):
            generator = func(*args, **kwargs)
            generator.__next__()
            return generator
        return wrapper

    @coroutine
    def printer():
        lineno = 1
        while True:
            value = yield
            print(f'{lineno}:\t{value}')
            lineno += 1

    generator = printer()
    for c in 'VERTICAL':
        generator.send(c)


example_coroutine()


def coroutine(func):
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        generator.__next__()
        return generator
    return wrapper


@example
def example_4():
    """
    Метод send также позволяет создавать конвейеры с помощью генераторов.

    Ранее рассматривался пример создания конвейера, где каждый следующий
    генератор принимал на вход поток данных в виде готового генератора,
    производил необходимые манипуляции, а затем возвращал новый поток данных.
    Структура конвейера основана на манипуляциями потоками данных.

    С использованием метода send структура конвейера основана на обработке
    событий, которые отправляются через send и обрабатываются генераторами.
    """
    def lines(filename, consumer):
        with open(filename, mode='r', encoding='UTF-8') as file:
            for line in file:
                consumer.send(line)

    @coroutine
    def grep(pattern, consumer):
        while True:
            item = yield
            if pattern in item:
                consumer.send(item)

    @coroutine
    def printer():
        while True:
            item = yield
            print(item)

    lines(
        'titanic.csv',
        grep(
            'Murray',
            printer()
        )
    )


example_4()


def lines(filename, consumer):
    with open(filename, mode='r', encoding='UTF-8') as file:
        for line in file:
            consumer.send(line)


@coroutine
def grep(pattern, consumer):
    while True:
        item = yield
        if pattern in item:
            consumer.send(item)


@coroutine
def printer():
    while True:
        item = yield
        print(item)


@example
def example_5():
    """
    Метод send позволяет удобно перенаправлять данные нескольким обработчикам.
    """
    @coroutine
    def broadcast(consumers):
        while True:
            item = yield
            for consumer in consumers:
                consumer.send(item)

    sink = printer()
    lines(
        'titanic.csv',
        broadcast([
            grep('Barbara', sink),
            grep('Christopher', sink),
            grep('Ramon', sink),
        ])
    )


example_5()
