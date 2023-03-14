import time


def format_time():
    """
    获取格式化的时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def print_with_time(*c):
    """
    带时间的打印
    """
    print(format_time() + " ".join(c))
