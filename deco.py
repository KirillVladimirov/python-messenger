def log(func):

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("{}({}, {}) = {}".format(func.__name__, args, kwargs, result))
        return result

    return wrapper


class Log():

    def __init__(self, number):
        self._num = number

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print("{}({}, {}) = {}".format(func.__name__, args, kwargs, result))
            print("=" * self._num)
            return result

        return wrapper


@log
def add(a, b):
    return a + b


@Log(50)
def multi(a, b):
    return a * b


add(10, 20)
multi(10, 20)
