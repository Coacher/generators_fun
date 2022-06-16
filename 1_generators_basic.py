#
# Generator expressions PEP-289
#

gen_exp = (x*x for x in [1, 2, 3, 4, 5])
print('gen_exp: ', gen_exp)  # generator object <genexpr> at 0x7ff866a65700>

# Возвращаемое значение -- итератор
# https://docs.python.org/3/glossary.html#term-generator-expression

# Итераторы:
# значения возвращаются ленивым образом;
# невозможно использовать после исчерпания (consume).

greatest = max(gen_exp)
# Вызывает исключение: ValueError: max() arg is an empty sequence
# greatest_too = max(gen_exp)

# Типовой пример использования: цикл for
gen_exp = (x*x for x in [1, 2, 3, 4, 5])  # Уже исчерпали выше
for square in gen_exp:
    print('square: ', square)

# Множество встроенных функций используют итераторы: map, filter, sum, etc.
# Целая встроенная библиотека для различных вкусностей: itertools

# Итераторы удобно комбинировать в конвейер

# Найти в файле слово Canary в строке комментария, заменить его на Птенчик
source = open('1_generators_basic.py', mode='r', encoding='UTF-8').readlines()
comments = filter(lambda x: x.startswith('#'), source)
has_canary = filter(lambda x: 'Canary' in x, comments)
translated = map(lambda x: x.replace('Canary', 'Птенчик'), has_canary)
print(list(translated))

# Под капотом:
# - для получения очередного значения из итератора вызывается метод __next__(),
# - при исчерпании итератора вызывается исключение StopIteration.
# Итератор -- это (почти) в точности объект, поддерживающий данный интерфейс.
#
# Можно эквивалентным образом вызывать __next__() встроенной функцией next()
# Встроенные средства языка для итераторов корректно обрабатывают StopIteration
gen_exp = (x*x for x in [1, 2])  # Уже исчерпали выше
# Можно так
print('__next__(): ', gen_exp.__next__())
# Но так удобнее
print('    next(): ', next(gen_exp))
# Вызывает исключение StopIteration
# print('next():', next(gen_exp))


#
# Генераторы (generators) -- функции с ключевым словом yield в определении.
#

def countdown(x):
    print('Countdown start')

    while x > 0:
        yield x
        x -= 1

    print('Boom!')


# Вызов генератора не приводит к началу выполнение его кода
gen_fun = countdown(3)
print('gen_fun: ', gen_fun)  # <generator object countdown at 0x7f719e549850>

# Чтобы заставить генератор работать, нужно по нему итерироваться.
# Можно так
n = gen_fun.__next__()
print(n)
# Но так удобнее
n = next(gen_fun)
print(n)

n = next(gen_fun)
print(n)

# Завершение тела генератора вызывает исключение StopIteration
try:
    print('Завершение тела генератора')
    n = next(gen_fun)
    print(n)
except StopIteration as exc:
    import traceback
    traceback.print_exception(exc)


# Генераторы:
# 1. Генератор -- функция с ключевым словом yield в определении
# 2. Вызов генератора не приводит к выполнению его кода, возвращает итератор
# 3. Выполнение кода генератора начинается при начале итерации
# 4. Выполнение кода останавливается на очередном yield, состояние сохраняется
# 5. При очередной итерации выполнение кода продолжается с момента остановки
# 6. Выход из генератора вызывает StopIteration

# Можно использовать return в генераторе, значение передается в StopIteration
def terminator():
    yield 'Hasta la vista, baby!'
    return 'I`ll be back!'


arnold = terminator()

print(next(arnold))

try:
    next(arnold)
except StopIteration as exc:
    import traceback
    traceback.print_exception(exc)
