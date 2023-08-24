import sys
import time


def format_time():
    """
    获取格式化的时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def log_d(*objs):
    """
    打印标准日志, 在Yyds.Auto一般日志显示为灰色
    """
    print(format_time() + "\t" + " ".join([str(i) for i in objs]), file=sys.stdout)


def log_e(*objs):
    """
    打印错误日志, 在Yyds.Auto一般日志显示为红色
    """
    print(format_time() + "\t" + " ".join([str(i) for i in objs]), file=sys.stderr)
