import traceback
import time
from functools import wraps, partial
from yydskernel import device_foreground_activity
from util import print_with_time


def try_run(func, print_exeception=True):
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


_ACTIVITY_HANDLER = dict()


def get_activity_handler(name: str):
    return _ACTIVITY_HANDLER[name]


def run_activity_handler(name: str):
    def run(func):
        @wraps(func)
        def run_func(*args, **kwargs):
            global _ACTIVITY_HANDLER
            _ACTIVITY_HANDLER[name] = partial(func, *args, **kwargs)
            cur = device_foreground_activity()
            if len(cur) < 1:
                time.sleep(2)
                cur = device_foreground_activity()
            if name == cur:
                print(f"⇛ 执行, 当前界面:{cur}")
                return _ACTIVITY_HANDLER[name]()
            else:
                print(f"⇛ 跳过执行, 期望:{name} 当前界面:{cur}")
                return None

        return run_func()

    return run


def do(times: int, interval: float, pre_interval=False, *func):
    if isinstance(pre_interval, bool) and pre_interval:
        time.sleep(pre_interval)
    for i in range(times):
        for f in func:
            f()
        time.sleep(interval)


def loop_activity_handle(other):
    while True:
        time.sleep(1)
        activity = device_foreground_activity()
        if activity in _ACTIVITY_HANDLER:
            _ACTIVITY_HANDLER[activity]()
        else:
            if other is not None:
                other()
            else:
                print_with_time("⇛ 未匹配界面:" + activity)
                break


def run_until_true(func, max_times):
    for i in range(max_times):
        print_with_time(f"⇛ 执行直至成功{i}:")
        if func():
            break
