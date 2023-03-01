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
    for i in range(1, 20):
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


def test_input_search():
    """
    比如在今日头条输入并搜索 "你好坏啊, 我好喜欢"
    """
    x_input_text("你好坏啊, 我好喜欢")
    key_confirm()


def main():
    """
    main 函数为入口，不可更改此函数名！此函数会被导入执行，无须在工程主动运行
    :return:
    """
    print("=" * 40)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " 开始运行")
    # test_output()
    # test_exception()

    # 点击坐标
    # click(1, 10)

    # 滑动
    # swipe(100, 200, 500, 1030, 500)

    # 控件匹配, 匹配屏幕中间往下所有文字不为空的控件
    # print(ui_match(text=".+", top=0.5))

    # 根据id查找控件
    # print(ui_match(resource_id="com.miui.home:id/clearAnimView"))

    # 指定区域进行 OCR 识别, 使用 gpu 进行运算识别, 屏幕从左到右300像素开始进行识别
    # print(screen_ocr(x=300, use_gpu=True))

    # 指定区域 OCR, 查找指定文字
    #print(screen_ocr_x(list("酷安"), y=0.1, h=400))

    # 找图
    # print(screen_find_image_x(("/img.area_llq.jpg", "pdd.jpg", "setting.jpg", ), x=0.2, y=300))
    # key_home()

    # 按下菜单键
    # key_menu()

    print("--")




