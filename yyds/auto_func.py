import traceback
import time
from functools import wraps, partial
from .auto_api_aux import device_foreground_activity


class WrapRecord:
    """
    界面与TASK的注册记录, 从c++角度来看, 我们这里存着一些函数指针, 需要的时候跳过去执行
    """
    ACTIVITY_HANDLER = dict()
    TASK_HANDLER = dict()


def try_run(func, print_exception=True):
    """
    :param func 函数
    :param print_exception 是否打印函数运行异常
    运行func函数, 并且捕抓其运行异常
    """
    try:
        return func()
    except:
        if print_exception:
            print(traceback.format_exc())
        return None


def run(func):
    """
    装饰器 直接运行定义的函数
    """

    @wraps(func)
    def run_func(*args, **kwargs):
        return func(*args, **kwargs)

    return run_func()


def run_no_hurt(func):
    """
    装饰器 直接运行定义的函数, 并捕抓其运行异常
    """

    @wraps(func)
    def run_func(*args, **kwargs):
        return func(*args, **kwargs)

    try:
        return run_func()
    except:
        print(traceback.format_exc())
        return None


def retry_until_true(retry_time=40, interval=1):
    """
    装饰器 循环运行定义的函数, 最大尝试`retry_time`次, 间隔`interval`秒,
    若在循环过程中, 函数返回结果为真, 则提前终止循环
    """

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


def register_task(*task_name):
    """
    :param task_name 任务名字
    把一个函数当作一个任务
    装饰器 注册任务
    """

    def run(func):
        @wraps(func)
        def run_func(*args, **kwargs):
            for t in task_name:
                WrapRecord.TASK_HANDLER[t] = partial(func, *args, **kwargs)
            return partial(func, *args, **kwargs)

        return run_func()

    return run


def handle_task(task_name: str):
    """
    :param task_name 任务名字
    执行处理`register_task`注册的任务
    """
    if task_name in WrapRecord.TASK_HANDLER:
        WrapRecord.TASK_HANDLER[task_name]()


def get_activity_handler(name: str):
    """
    把每一个界面当作一个任务
    """
    return WrapRecord.ACTIVITY_HANDLER[name]


def run_activity_handler(*names: str):
    """
    :param names 注册的活动名, 可变参数, 即可同时注册多个
    判断当前设备活动名是否为注册的活动名, 如果是, 则执行任务, 如果不是, 则打印日志
    """

    def run(func):
        @wraps(func)
        def run_func(*args, **kwargs):
            cur = device_foreground_activity()
            for name in names:
                WrapRecord.ACTIVITY_HANDLER[name] = partial(func, *args, **kwargs)

                if len(cur) < 1:
                    time.sleep(2)
                    cur = device_foreground_activity()
                if name == cur:
                    print(f"⇛ 执行, 当前界面:{cur}")
                    return WrapRecord.ACTIVITY_HANDLER[name]()
                else:
                    print(f"⇛ 跳过执行, 期望:{name} 当前界面:{cur}")
                    continue

        return run_func()

    return run


def do(times: int, interval: float, pre_interval: bool, *func):
    """
    高级函数 循环并且间隔n秒执行一箩筐的函数, 或许能够显得代码工整点吧~
    :param times 执行次数
    :param interval 执行间隔秒数
    :param func 可变参数, 执行的函数
    """
    if isinstance(pre_interval, bool) and pre_interval:
        time.sleep(pre_interval)
    for i in range(times):
        for f in func:
            f()
        time.sleep(interval)


def loop_activity_handle(other):
    """
    :param other
    把脚本主循环交给界面处理器, 当手机在不同的界面时, 会执行不同的函数
    """
    while True:
        time.sleep(1)
        activity = device_foreground_activity()
        if activity in WrapRecord.ACTIVITY_HANDLER:
            WrapRecord.ACTIVITY_HANDLER[activity]()
        else:
            if other is not None:
                other()
            else:
                log_d("⇛ 未匹配界面:" + activity)
                break


def run_until_true(func, max_times: int):
    """
    高级函数
    :param func 函数
    :param max_times 次数
    最大尝试max_times次运行func, 如果结果为真, 则立马返回
    """
    for i in range(max_times):
        log_d(f"⇛ 执行直至成功{i}:")
        if func():
            break
