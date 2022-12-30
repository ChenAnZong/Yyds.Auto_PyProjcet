import traceback
from functools import wraps


def try_run(func, print_exeception = True):
    try:
        return func()
    except:
        if print_exeception:
            print(traceback.format_exc())
        return None


def run(func):
    @wraps(func)
    def run_func(*args, **kwargs):
        return func(*args, **kwargs)
    return run_func()


def run_no_hurt(func):
    @wraps(func)
    def run_func(*args, **kwargs):
        return func(*args, **kwargs)
    try:
        return run_func()
    except:
        print(traceback.format_exc())
        return None


def retry_until_true(retry_time=40, interval=1):
    def decorate(func):
        rc = 0
        run_result = False

        @wraps(func)
        def run_func(*args, **kwargs):
            print('⇛ [{retry_count}] retry({name}) '.format(retry_count=rc, name=func.__name__))
            return func(*args, **kwargs)

        while not run_result and rc < retry_time:
            time.sleep(interval)
            run_result = run_func()
            rc += 1
        return run_result
    return decorate