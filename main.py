import os
import json
import sys
import threading
import pickle
import codecs
import time
import funfunc
from PIL import Image
# import flask
# import websockets
import yyds
import flask
import importlib

from yyds import *


def test_output():
    for i in range(1, 100):
        time.sleep(1)
        print(f"循环输出:{i}")


# 类定义示例
class Person:
    def __init__(self, n, a):
        self.name = n
        self.age = a

    def show(self):
        print(self.name + "_" + str(self.age))


aa: Person


def test_cache():
    """
    测试缓存配置
    :return:
    """
    global aa
    aa = Person("chenMoney", 2)
    aa.show()
    f = open('.cache', mode='wb+')
    pickle.dump(aa, f, 0)
    f.close()

    print("测试反序列执行，如果输出信息，则正常")
    f = open('.cache', mode='rb')
    bb = pickle.load(f)
    f.close()
    bb.show()


def test_exception():
    a = 1 / 0


def test_env():
    print("当前运行Py文件:" + __file__)
    print("代码工作目录:" + os.getcwd())
    print(f"当前线程: {threading.current_thread().native_id}")

    # 装饰器测试
    @funfunc.run_no_hurt
    def may_raise_error():
        print("测试装饰器")
        test_exception()

    with codecs.open("content.txt", mode="r") as fr:
        print("读取文件内容:" + fr.read())


def main():
    """
    main 函数为入口，不可更改此函数名！此函数会被导入执行，无须在工程主动运行
    :return:
    """
    print("==============11")
    # print(screen_ocr_first_x("蓝牙"))
    # print(screen_find_image_x(("img/area_llq.jpg", "img/pdd.jpg", "img/setting.jpg",)))
    print("是否存在11:", ui_match(text="水果看看"))





