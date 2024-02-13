import sys
import time


def format_time():
    """
    获取格式化的时间, 格式样式如:2024.02.04 12:56:31
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def log_d(*objs):
    """
    打印标准日志, 在Yyds.Auto开发插件中一般日志显示为灰色
    """
    print(format_time() + "\t" + " ".join([str(i) for i in objs]), file=sys.stdout)


def log_e(*objs):
    """
    打印错误日志, 在Yyds.Auto开发插件中一般日志显示为红色
    """
    print(format_time() + "\t" + " ".join([str(i) for i in objs]), file=sys.stderr)
