def start_end(func):
    """print start and end of func"""

    def inner():
        print('-- %s start --' % func.__name__)
        result = func()
        print('-- %s end --\n' % func.__name__)
        return result
    return inner
