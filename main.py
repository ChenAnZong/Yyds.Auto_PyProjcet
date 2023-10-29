"""
@author  玩机达人 微信:wjzy_yyds
@desc    Yyds.Auto 官方封装Python函数 更多用法 https://yydsxx.com
@tip     _x结尾系列为高级封装函数, 一般使用此类函数; _开头为内部函数, 一般不对外使用
@version 对应 Yyds.Auto 版本: 78(5.2)
"""
import os
import json
import sys
import threading
import pickle
import codecs
import time
import colorsys
from PIL import Image

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

    # 避免这个函数抛异常中断代码
    @run_no_hurt
    def may_raise_error():
        print("测试装饰器")
        test_exception()

    with codecs.open("content.txt", mode="r") as fr:
        print("读取文件内容:" + fr.read())


def test_input_search():
    """
    比如在今日头条输入并搜索 "你好坏啊, 我好喜欢"
    """
    # 一般来说, 我们使用输入法输入文字到编辑框的时候, 应当先清理当前编辑框文本, 以符合输入预期, 否则在已经有的内容后面追加输入
    x_input_clear()
    x_input_text("你好坏啊, 我好喜欢")
    key_confirm()


def main_():
    # 初始化设备屏幕参数以便使用坐标缩放以及随机性触摸函数
    DeviceScreen.init()

    # 往上滑动
    # swipe_up()
    log_d("=+" * 20)
    # 获取前台包名
    log_d(device_foreground_package())
    # 获取前台应用界面名
    log_d(device_foreground_activity())

    # bring_app_to_top("com.android.browser")
    log_d(is_app_running("com.android.browser"))

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
    # print(ocr(x=300, use_gpu=True))

    # 指定区域 OCR, 查找指定文字
    # print(screen_ocr_x(list("酷安"), y=0.1, h=400))

    # 找图
    # print(screen_find_image_x(("/img.area_llq.jpg", "pdd.jpg", "setting.jpg", ), x=0.2, y=300))
    # key_home()

    # 按下菜单键
    # key_menu()

    # 获取用户的配置键值
    # print(Config.read_config_value("select-1"))

    # 读取ui.yml的值, 注意select返回为数组
    # print(Config.read_ui_value("select-1"))

    # print(ui_match(resource_id="com.wj.play:id/image_icon_con"))
    # 如果 ui没有改变, 则可以从缓存匹配, 加快匹配速度
    # print(ui_match(True, height="<50", width="<50"))

    # 获取ui控件的中间坐标
    # print(ui_match(resource_id="com.wj.play:id/image_icon_con")[0].center_point)

    # 设置配置键值
    # Config.write_config_value("edit-user", "陈主任")

    # 寻找所有图片，最小相似度为0.7，如发现则点击
    find_image_click_max_prob(
        "ttxcy/开启转盘.jpg",
        "ttxcy/收下.jpg",
        "ttxcy/疯狂大转盘.jpg",
        min_prob=0.7
    )

    # 发现以下ocr文字则进行点击
    ocr_click_any("允许", "禁止", "取消安装")
    # 指定文字搜寻点击
    ocr_click_if_found("搜全网.*?", w=0.2, h=0.3)

    # 重试10次查找页面1， 间隔3秒，如发现则返回
    @run_until_true(10, 3)
    def 等待页面1():
        if screen_find_image_x("img/111.jpg"):
            return True
        else:
            return False

    # 进入页面1失败，抛出异常中断代码
    assert 等待页面1

    # 打开app
    # open_app("com.coolapk.market")

    # 抛出SystemExit异常，中断代码执行
    # exit(0)


def main():
    engine_set_debug(True)
    log_d("===开始脚本执行! 以下是对79版本对图色类函数测试")
    log_d("获取坐标颜色:", get_color(979, 611))
    # 如下, 我们查找yyds.auto app上面两个绿色勾勾的位置!
    log_d("颜色查找:", find_color("33,146,38", max_fuzzy=10, y=.2, x=.7, max_counts=6, step_y=80))
    if os.path.exists("/sdcard/1.jpg") and os.path.exists("/sdcard/2.jpg"):
        log_d("图片相似度:", image_similarity("/sdcard/1.jpg", "/sdcard/2.jpg"))
    log_d("图片多次匹配:", match_images(template_image="img/gou.jpg", threshold=0, prob=0.8))

    log_d("多点找色1:",
          find_color("7,203,117"))
    log_d("多点找色2:",
          find_color("7,203,117", bias_points=["-313,0|~243,46,14"], max_fuzzy=20))


"""
1. main 函数为Yyds.Auto工程的入口，不可更改此函数名！此函数会被导入执行，无须在工程主动运行
2.如果代码有BUG 请联系作者24小时内处理解决
"""
