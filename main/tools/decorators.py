import time


def get_time_consume(f):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        print(f.__qualname__, '耗时：{}秒'.format(e_time - s_time))
        return res

    return inner


