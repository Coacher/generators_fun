# Generator expressions (PEP-289)
# Определение:
#   https://docs.python.org/3/glossary.html#term-generator-expression
# Синтаксис:
#   https://docs.python.org/3/reference/expressions.html#generator-expressions
from traceback import print_exception

from common import example


@example
def example_1():
    """
    Generator expressions возвращают итератор (iterator).

    Итераторы (PEP-234)
    Определение:
        https://docs.python.org/3/glossary.html#term-iterator
    Протокол:
        https://docs.python.org/3/library/stdtypes.html#typeiter

    Итераторы:
        - абстрация над потоком данных;
        - значения возвращаются ленивым образом при вызове метода __next__;
        - после исчерпания вызов __next__ вызывает исключение StopIteration;
        - невозможно использовать повторно после исчерпания.
    """
    iterator = (x*x for x in range(1, 6))

    print(iterator)


example_1()


@example
def example_2():
    """
    Для получения очередного значения из итератора используется метод __next__
    или встроенная функция next.
    """
    iterator = (x*x for x in range(1, 6))

    print(iterator.__next__())
    print(next(iterator))
    print(iterator.__next__())
    print(next(iterator))


example_2()


@example
def example_3():
    """
    При исчерпания генератора вызовы метода __next__ или функции next вызывают
    исключение StopIteration.
    """
    short = (x*x for x in range(1, 2))

    try:
        print(next(short))
        print(next(short))
    except StopIteration as exc:
        print_exception(exc)


example_3()


@example
def example_4():
    """
    Типовой пример использования итераторов -- цикл for.
    Множество встроенных функций поддерживают итераторы: map, filter, sum, etc.
    Существует встроенная библиотека для работы с итераторами: itertools.

    Во всех этих случаях не надо беспокоиться об обработке StopIteration.
    """
    iterator = (x*x for x in range(1, 6))

    for i in iterator:
        print(f'A square: {i}')


example_4()


@example
def example_5():
    """
    Итераторы являются представлением потока данных. Как следствие, их удобно
    соединять друг за другом в конвейер, подобно конвейерам в Unix оболочках.
    """
    # Пример: найти слово Canary в комментариях, заменить его на слово Птенчик.
    #
    # В данном конвейере все операции происходят ленивым образом, исходный файл
    # и все промежуточные данные не загружаются в память полностью.
    #
    # Получить строки данного файла в виде итератора
    strs = iter(open('1_generator_expressions.py', mode='r', encoding='UTF-8'))
    # Выбрать среди строк только комментарии
    comments = filter(lambda x: x.lstrip().startswith('#'), strs)
    # Выбрать среди комментариев строки со словом Canary
    canaries = filter(lambda x: 'Canary' in x, comments)
    # Заменить в полученных строках слово Canary на слово Птенчик
    replaced = map(lambda x: x.replace('Canary', 'Птенчик'), canaries)

    print(*list(replaced), sep='')


example_5()
