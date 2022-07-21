from common import example


@example
def example_1():
    """
    Генераторы позволяют реализовывать бесконечные последовательности данных.

    Например, данный генератор представляет последовательность простых чисел.
    """
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

    generator = primes()
    for i in range(1, 11):
        print(f'{i}-th prime is {next(generator)}')


example_1()
