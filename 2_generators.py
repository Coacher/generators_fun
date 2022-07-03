# Generators (PEP-255, PEP-342)
# Определение:
#   https://docs.python.org/3/glossary.html#term-generator
from traceback import print_exception

from common import example


@example
def example_1():
    """
    Генератор -- функция с ключевым словом yield в определении.

    Генераторы возвращают generator iterators, которые полностью поддерживают
    протокол итераторов, подробно рассмотренный ранее. Как следствие, поведение
    генераторов во многом похоже на generator expressions.
    """
    def countdown(x):
        print('Countdown start!')

        while x > 0:
            yield x
            x -= 1

        print('BOOM!')

    # Вызов генератора не приводит к началу выполнения его кода.
    generator = countdown(5)
    print(generator)
    print('# Вызвали генератор')

    # Чтобы заставить генератор работать, нужно начать по нему итерироваться.
    print('# Начали итерироваться')
    print(generator.__next__())
    print(next(generator))
    print(generator.__next__())
    print(next(generator))

    # Завершение кода генератора вызывает исключение StopIteration.
    try:
        print('# Исчерпали генератор')
        print(next(generator))
        print(next(generator))
    except StopIteration as exc:
        print_exception(exc)


example_1()


@example
def example_2():
    """
    В теле генератора допустимо использовать return. В момент выхода из тела
    генератора автоматически вызывается исключение StopIteration. Возвращаемое
    через return значение используется при создании экземпляра StopIteration.
    """
    def terminator():
        yield 'Hasta la vista, baby!'
        return 'I`ll be back!'

    arnold = terminator()

    try:
        print(next(arnold))
        print(next(arnold))
    except StopIteration as exc:
        print_exception(exc)


example_2()


@example
def example_3():
    """
    В Python 3 можно использовать конструкцию yield from для возвращения
    значений из существующего итератора. Управление не передается дальше
    пока итератор не будет исчерпан.
    """
    def generator():
        yield from range(-3, 0, 1)
        yield from range(0, 3, 1)

    print(list(generator()))


example_3()


@example
def example_4():
    """
    Генераторы позволяют создавать конвейеры со сколь угодно сложной логикой.

    В отличие от generator expressions можно повторно использовать общую логику
    без дублирования исходного кода. При этом сохраняются преимущества ленивых
    вычислений.
    """
    # Пример: найти выживших женщин старше 18 среди пассажиров 1го класса.
    #
    # Получить строки файла с данными о пассажирах в виде итератора.
    # Здесь намеренно не используется стандартный модуль csv, чтобы показать
    # больше возможностей работы с генераторами.
    def lines(filename):
        with open(filename, mode='r', encoding='UTF-8') as file:
            yield from iter(file)

    # Преобразовать каждый элемент в словарь для удобного доступа
    def tokens(stream):
        tokens = ('name', 'class', 'age', 'sex', 'survived')
        for item in stream:
            name, *values = item.strip().rsplit(',', maxsplit=4)

            last, _, first = name.strip('"').partition(', ')
            name = f'{first} {last}'

            yield dict(zip(tokens, (name, *values)))

    # Аналог SQL фильтра WHERE
    def where(key, value, stream):
        for item in stream:
            if item[key] == value:
                yield item

    # Аналог SQL функции NVL
    def nvl(key, default, stream):
        for item in stream:
            if not item[key]:
                item[key] = default
            yield item

    source = lines('titanic.csv')

    entries = tokens(source)

    first_class = where('class', '1st', entries)

    females = where('sex', 'female', first_class)

    survivors = where('survived', '1', females)

    # Не для всех пассажиров есть данные о возрасте,
    # при отсутствии данных считаем возраст равный 0.
    survivors = nvl('age', '0', survivors)

    adults = filter(lambda x: float(x['age']) >= 18, survivors)

    print('First 10 entries without any special ordering:')
    print(*[x['name'] for x in adults][:10], sep='\n')


example_4()
