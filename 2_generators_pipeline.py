# Развлекательный пример №1: генератор бесконечной последовательности
def squares():
    n = 1
    while True:
        yield n*n
        n += 1


for number, square in enumerate(squares(), start=1):
    print(number, square)
    if number >= 100:
        break


# Развлекательный пример №2: решето Эратосфена
def primes():
    yield 2
    yield 3
    sieve = [2, 3]

    while True:
        candidate = sieve[-1]
        while True:
            candidate += 2
            for prime in sieve[:-1]:
                if candidate % prime == 0:
                    break
            else:
                yield candidate
                sieve.append(candidate)
                break


for number, prime in enumerate(primes(), start=1):
    print(number, prime)
    if number >= 150:
        break


# Полезный пример: парсинг файлов с фильтрацией и обработкой записей а-ля SQL
def lines(path):
    with open(path, mode='r', encoding='UTF-8') as file:
        for line in file:
            yield line


def tokenize(lines):
    tokens = ('name', 'class', 'age', 'sex', 'survived')
    for line in lines:
        name, *values = line.strip().rsplit(',', maxsplit=4)

        last, _, first = name.strip('"').partition(', ')
        name = f'{first} {last}'

        yield dict(zip(tokens, (name, *values)))


def where(key, value, entries):
    for entry in entries:
        if entry[key] == value:
            yield entry


def nvl(key, default, entries):
    for entry in entries:
        if not entry[key]:
            entry[key] = default
        yield entry


source = lines('titanic.csv')

entries = tokenize(source)

females = where('sex', 'female', entries)

survivors = where('survived', '1', females)

adults = filter(lambda x: float(x['age']) >= 18, nvl('age', '0', survivors))

for x in adults:
    print(x['name'])
