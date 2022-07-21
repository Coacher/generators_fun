# Generator methods: close (PEP-342, PEP-479)
# Описание:
#   https://docs.python.org/3/reference/expressions.html#generator.close
from traceback import print_exception

from common import example, make_header


@example
def example_1():
    """
    Генераторы имеют специальный метод close, который завершает генератор.

    С точки зрения интерфейса, после закрытия генератора попытка получить
    из него значение вызывает исключение StopIteration, аналогично случаю
    исчерпания генератора. Если генератор уже исчерпан, вызов метода close
    не имеет никакого эффекта.

    С точки зрения реализации, при вызове метода close внутри генератора
    в текущей сохраненной точке выполнения вызывается исключение GeneratorExit.

    ВАЖНО: в отличие от StopIteration класс GeneratorExit является дочерним
    классом BaseException, но не Exception.
    """
    def hundred():
        try:
            yield from range(100)
        except BaseException as err:
            print(make_header('Caught exception inside generator', filler='*'))
            print_exception(err)
            raise err

    generator = hundred()
    try:
        print(next(generator))
        print(next(generator))
        generator.close()
        print('Generator closed')
        print(next(generator))
    except Exception as err:
        print(make_header('Caught exception outside of generator', filler='*'))
        print_exception(err)


example_1()


@example
def example_2():
    """
    Обработка GeneratorExit внутри генератора возможна по одному из сценариев:
      - никакой обработки, исключение GeneratorExit поднимается наружу;
      - перехват исключения GeneratorExit, которое затем поднимается наружу;
      - перехват исключения GeneratorExit, выход из генератора через return.
    """
    def noop_on_close():
        print('Noop start')
        yield from range(10)
        print('Noop finish')

    gen = noop_on_close()
    next(gen)
    gen.close()

    def reraise_on_close():
        print('Reraise start')
        try:
            yield from range(10)
        except GeneratorExit as err:
            print(f'Reraising {err!r}')
            print('Reraise finish')
            raise err

    gen = reraise_on_close()
    next(gen)
    gen.close()

    def return_on_close():
        print('Return start')
        try:
            yield from range(10)
        except GeneratorExit:
            retval = 'Goodbye!'  # Не будет доступно снаружи.
            print(f'Returning {retval!r}')
            print('Return finish')
            return retval

    gen = return_on_close()
    next(gen)
    gen.close()


example_2()


@example
def example_3():
    """
    Обработка GeneratorExit по одному из следующих сценариев является ошибкой:
      - перехват исключения GeneratorExit, возврат значения через yield,
      - перехват исключения GeneratorExit, вызов исключения StopIteration.

    ВАЖНО:
      - несмотря на утверждение "If the generator raises any other [other than
        GeneratorExit] exception, it is propagated to the caller." в описании
        https://docs.python.org/3/reference/expressions.html#generator.close,
      - несмотря на псевдокод, приведенный в PEP-342
        https://peps.python.org/pep-0342/#new-generator-method-close,
    перехват исключения GeneratorExit и вызов исключения StopIteration вместо
    него является ошибкой и приводит к RuntimeError, см. PEP-479.
    """
    def yield_on_close():
        print('Yield start')
        try:
            yield from range(10)
        except GeneratorExit:
            retval = 'Goodbye!'
            print(f'Yielding {retval!r}')
            yield retval
        finally:
            print('Yield finish')

    gen = yield_on_close()
    next(gen)
    try:
        gen.close()
    except BaseException as err:
        print_exception(err)

    def stopiter_on_close():
        print('Stopiter start')
        try:
            yield from range(10)
        except GeneratorExit:
            retval = 'Goodbye!'
            print(f'Raising StopIteration({retval!r})')
            raise StopIteration(retval)
        finally:
            print('Stopiter finish')

    gen = stopiter_on_close()
    next(gen)
    try:
        gen.close()
    except BaseException as err:
        print(f'Outer scope received {err!r}')
        print_exception(err)


example_3()


@example
def example_4():
    """
    Вызов исключения, отличного от StopIteration и GeneratorExit, приводит
    к завершению генератора, а исключение поднимается наружу обычным образом.
    """
    def raise_on_close():
        print('Raise start')
        try:
            yield from range(10)
        except GeneratorExit:
            err = NotImplementedError()
            print(f'Raising {err!r}')
            raise err
        finally:
            print('Raise finish')

    gen = raise_on_close()
    next(gen)
    try:
        gen.close()
    except BaseException as err:
        print(f'Outer scope received {err!r}')
        print_exception(err)


example_4()


@example
def example_5():
    """Перехват исключения GeneratorExit полезен для освобождения ресурсов."""
    resource_is_busy = False

    def read_from_resource():
        nonlocal resource_is_busy
        resource_is_busy = True
        try:
            yield from range(10)
        except GeneratorExit:
            resource_is_busy = False
            raise

    gen = read_from_resource()
    print(f'Resource is busy? {resource_is_busy}')
    next(gen)
    print(f'Resource is busy? {resource_is_busy}')
    gen.close()
    print(f'Resource is busy? {resource_is_busy}')


example_5()
