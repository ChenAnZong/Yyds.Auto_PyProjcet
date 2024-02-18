import json
import yaml
import shutil
import sys
import time
import traceback
import requests
import os
import random
import re
import hashlib
import importlib
from typing import Union, Tuple, List, Optional
from .auto_entity import *
from .util import log_d
from .util import log_e


class ProjectEnvironment:
    """
    当前工程的运行环境, 工程级的全局变量
    """
    # 默认的截图保存目录
    DEFAULT_SCREEN_SHOT_PATH = "/sdcard/screenshot.png"
    # 默认的控件信息抓取保存目录
    DEFAULT_UI_DUMP_PATH = "/data/local/tmp/dump.xml"
    # 当前手机运行的工程目录
    CWD = os.getcwd()
    # 在开发中, 如果是调试模式, 将会打印更多日志
    DEBUG_MODE = False
    PROJECT_NAME = ""
    DEBUG_IP = ""
    IMPORT_JAVA_SUCCESS = False  # IMPORT_JAVA_SUCCESS == Ture 我们可以认定当前代码使用手机引擎运行, 否则在电脑上运行
    # 全局配置(包括ui配置)
    GLOBAL_CONFIG = dict()

    @classmethod
    def current_project(cls) -> str:
        """
        返回当前正在运行的工程目录名(目录名不一定与工程名字相同, 目录名具有唯一性)
        在引擎内部, 将工程目录名视为唯一ID
        """
        if cls.IMPORT_JAVA_SUCCESS:
            return os.path.basename(cls.CWD)
        else:
            return cls.PROJECT_NAME

    @classmethod
    def current_project_dir(cls) -> str:
        """
        返回当前手机上正在运行的工程目录
        """
        return f"/sdcard/Yyds.Py/{cls.current_project()}"


class Config:
    """
    可视作一个小型的配置存储类, 并与设备的ui的配置共享同一个存储位置
    所有配置序列化为将配置保存为json格式, 如需读写大量数据, 请使用 👉`sqlite`
    """

    @classmethod
    def get_config_path(cls) -> str:
        return f"/sdcard/Yyds.Py/config/{ProjectEnvironment.current_project()}.json"

    @classmethod
    def reload_config(cls):
        try:
            with open(cls.get_config_path(), mode="r") as fr:
                ProjectEnvironment.GLOBAL_CONFIG = json.loads(fr.read())
        except:
            pass

    @classmethod
    def read_config_value(cls, config_name: str, read_load=False) -> Union[bool, str, int, None]:
        """
        可同时获取ui配置键值，其中 select(字符串值配置)、edit(字符串值配置)、check(布尔值配置)为配置值与非ui配置键值。

        edit-user:
          \t title: "账号"\n
          \t value: "输入您的账号"

        如 ui 配置如上，则使用 read_config_value("edit-user") 进行获取。

        如果不存在config_name或config_name不可配置，则返回 None.

        :param config_name: ui名字
        :param read_load: 是否重新读取配置
        :returns: 返回值的解释⚠️
                     - bool: 如果用户未进入ui界面进行配置，则返回None，脚本需要判断并设置某些默认的值
                     - str: 返回字符串类型值
                     - int: 返回整数类型值
        :rtype: Union[bool, str, int, None]
        """
        # 判断是否要进行重新读取
        if read_load or len(ProjectEnvironment.GLOBAL_CONFIG) == 0:
            cls.reload_config()
        if config_name in ProjectEnvironment.GLOBAL_CONFIG and not read_load:
            return ProjectEnvironment.GLOBAL_CONFIG[config_name]
        if config_name in ProjectEnvironment.GLOBAL_CONFIG:
            return ProjectEnvironment.GLOBAL_CONFIG[config_name]
        else:
            return None

    @classmethod
    def write_config_value(cls, config_name: str, value):
        """
        利用代码保存配置 (一般比较少用)

        :param config_name: ui名字
        :param value: 值
        :returns: 无
        """
        with open(cls.get_config_path(), mode="w+") as frw:
            try:
                ProjectEnvironment.GLOBAL_CONFIG = json.loads(frw.read())
            except:
                pass
            ProjectEnvironment.GLOBAL_CONFIG[config_name] = value
            frw.write(json.dumps(ProjectEnvironment.GLOBAL_CONFIG, ensure_ascii=False))

    @classmethod
    def read_ui_value(cls, config_name: str) -> Union[str, None]:
        """
        直接从工程目录下的 ui.yml 文件读取 value, 利用这个读取函数, 我们可以在ui.yml中配置默认值
        :returns: 读取到的配置值
        """
        if not os.path.exists("ui.yml"):
            return None
        else:
            with open(r"ui.yml", mode="r", encoding="utf-8") as fr:
                c = fr.read()
                y = yaml.unsafe_load(c)
                return y[config_name]["value"]


class EngineDebug:
    @staticmethod
    def _version() -> str:
        """
        自动化引擎 插件版本号, 即插件应用的app VersionCode
        """
        return engine_api("/version")

    @staticmethod
    def _pid() -> int:
        """
        :returns: 自动化引擎进程pid
        """
        return int(engine_api("/pid"))

    @staticmethod
    def _uid() -> int:
        """
        - uid = 0, 为ROOT 权限运行
        - uid = 2000, 为SHELL 权限运行

        :returns: 自动化引擎进程uid
        """
        return int(engine_api("/uid"))

    @staticmethod
    def _ping() -> bool:
        """
        自动化引擎 [调试使用] 插件自动化引擎rpc通讯检测
        :returns: 是否通讯成功
        """
        return engine_api("/ping") == "pong"

    @staticmethod
    def _reboot():
        """
        重启自动化引擎
        :returns: 无
        :raises: 因引擎
        """
        return engine_api("/reboot")

    @staticmethod
    def _exit():
        """
        结束自动化引擎
        """
        return engine_api("/exit")

    @staticmethod
    def _press_down(x, y):
        """
        模拟单个手指按下坐标

        :param x: x 坐标
        :param y: y 坐标
        """
        return engine_api("/press_down", {"x": x, "y": y})

    @staticmethod
    def _press_up(x, y):
        """
        模拟单个手指弹起坐标

        :param x: x 坐标
        :param y: y 坐标
        """
        return engine_api("/press_up", {"x": x, "y": y})

    @staticmethod
    def _press_move(x, y):
        """
        模拟单个手指移动坐标

        :param x: x 坐标
        :param y: y 坐标
        """
        return engine_api("/press_move", {"x": x, "y": y})

    @staticmethod
    def _reload_py_module(module_name):
        """
        指定重新加载某个python模块

        :param module_name 模块名
        """
        importlib.reload(sys.modules[module_name])


def engine_set_debug(is_debug: bool):
    """
    项目级别的调试标志

    :param is_debug: 是否打印与自动化引擎通讯的日志
    """
    ProjectEnvironment.DEBUG_MODE = is_debug


def __handle_screen_rect_args(args: dict, x=None, y=None, w=None, h=None):
    """
    内部调用 转化图片裁剪参数
    """
    if x is not None:
        args["x"] = x
    if w is not None:
        args["w"] = w
    if h is not None:
        args["h"] = h
    if y is not None:
        args["y"] = y


def __handle_image_path(image) -> str:
    """
    引擎需要传输绝对的文件路径作为参数, 如果传输为相对文件路径, 将转化为拒绝的文件路径
    """
    real_path = os.path.join(ProjectEnvironment.current_project_dir(), image) if os.path.exists(
        os.path.join(ProjectEnvironment.current_project_dir(), image)) else image
    return real_path


try:
    # 下面两句代码调用java, 与自动化引擎进行通讯, 在IDE中识别不到, 会提示错误请忽略!
    from uiautomator import ExportHandle as EngineApi
    from java.util import HashMap
    ProjectEnvironment.IMPORT_JAVA_SUCCESS = True
except:
    # 如果是PC环境运行, 会导入失败, 使用http与引擎进行通讯, 使用在电脑上可以正常运行代码
    from configparser import ConfigParser

    project_config = ConfigParser()
    # 读取调试机IP地址
    config_path = os.path.join(os.getcwd(), "project.config")
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(__file__), "../project.config")
    if not os.path.exists(config_path):
        raise RuntimeError("配置文件不存在:" + config_path)
    project_config.read(config_path)
    ProjectEnvironment.DEBUG_IP = project_config["default"]["DEBUG_DEVICE_IP"]
    ProjectEnvironment.PROJECT_NAME = project_config["default"]["PROJECT_NAME"]
    log_d(f"当前连接调试设备IP: {ProjectEnvironment.DEBUG_IP}")


def engine_api(uri: str, options=None) -> str:
    """
    🫶自动化引擎底层RPC调用接口, 如果在安卓中, 则进行反射调用; 如果在电脑上调用, 则使用http调用

    :param uri: 远程接口
    :param options: 参数，字典类型，所有键值都应为str类型
    :returns: 引擎返回的结果, 所有结果均由字符串进行表示, 一般后续需要进行一定的序列化处理
    """
    if options is None:
        options = {}
    if options is None:
        options = {}
    if ProjectEnvironment.IMPORT_JAVA_SUCCESS:
        params = HashMap()
        if options:
            for key in options.keys():
                params.put(key, str(options[key]))
        ret = EngineApi.http(uri, params)
    else:
        # 49009是引擎通讯端口
        ret = requests.post(f"http://{ProjectEnvironment.DEBUG_IP}:49009{uri}", json=options).text
    if ProjectEnvironment.DEBUG_MODE:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{t}:{uri}__{options}___))){ret})))))))\n")
    return ret


def click(x: Union[str, int], y: Union[str, int]):
    """
    点击坐标点

    :param x: 屏幕绝对坐标，不支持小数
    :param y: 屏幕绝对坐标，不支持小数
    """
    x += random.randint(-3, 3)
    y += random.randint(-5, 5)
    engine_api("/touch", {"x": int(x), "y": int(y)})


def random_click(x: int, y: int, w: int, h: int):
    """
    在指定区域内 随机点击 做到模拟人工操作

    :param x: X坐标
    :param y: Y坐标
    :param w: 在x坐标上, 可以横向偏移多少
    :param h: 在y坐标上, 可以纵向偏移多少
    """
    x = x
    y = y
    y += h * 0.25 + random.uniform(h * 0.25, h * 0.75)
    x += w * 0.25 + random.uniform(w * 0.25, w * 0.75)
    click(x, y)


def md5_file(path) -> str:
    """
    计算文件MD5

    :param path: 文件路径
    :returns: 32位md5计算结果
    """
    md5 = hashlib.md5()
    f = open(path, mode="rb")
    md5.update(f.read())
    f.close()
    md5_sum = md5.hexdigest()
    return md5_sum


def md5_str(text) -> str:
    """
    计算文本MD5

    :param text: 文本内容
    :returns: 文本MD5
    """
    md5 = hashlib.md5()
    md5.update(text.encode("utf-8"))
    md5_sum = md5.hexdigest()
    return md5_sum


def toast(content: str):
    """
    :param content: 提示内容

    提示:某些机型需要打开 应用后台窗口弹出权限
    """
    engine_api("/toast", {"content": content})


def screenshot(path=None) -> str:
    """
    屏幕截图, 注意横屏截图与竖屏对截图对像素是不一样的

    :param path: 截图保存路径, 此接口无需申请任何权限
    :return: 截图对最终保存路径
    """
    if not path:
        path = ProjectEnvironment.DEFAULT_SCREEN_SHOT_PATH
    return engine_api('/screenshot', {"path": path})


def ocr(image=None, x=None, y=None, w=None, h=None, use_gpu=False) -> str:
    """
    [底层接口] 使用引擎识别当前屏幕的文字, 可指定识别范围

    :param image: 若image==None, 则截取屏幕进行识别; 若image为文件路径, 则
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽
    :param h: 高
    :param use_gpu: 是否使用Gpu运算, 性能差的手机不建议, 会导致手机掉帧
    :returns: 引擎返回识别文本
    """
    args = {"use_gpu": "true" if use_gpu else "false"}
    __handle_screen_rect_args(args, x, y, w, h)
    if image is None:
        return engine_api("/screen-ocr", args)
    elif isinstance(image, str):
        image_path = __handle_image_path(image)
        args["path"] = image_path
        return engine_api("/image-ocr", args)


def screen_yolo_locate(x=None, y=None, w=None, h=None, use_gpu=True) -> str:
    """
    [底层接口] 底层接口 使用yolo查找目标

    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param use_gpu: 是否使用gpu运行，建议处理器较差的机器不要使用gpu运算，会卡顿
    :returns: 引擎返回识别文本
    """
    args = {"use_gpu": "true" if use_gpu else "false"}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/key-locate", args)


def screen_find_image(*img, x=None, y=None, w=None, h=None, threshold: int = -1) -> str:
    """
    [底层接口] 在屏幕上同时寻找多张图片, 可以指定范围\n

    使用例子(从屏幕中间往下(1920*0.2)高度, 左边100像素开始寻找, 若分辨率 h=1920):
    :: python
        screen_find_images("/sdcard/1.png;/sdcard/2.png", y=960, h=0.2, x=100)

    :param img: 图片路径, 建议使用相对路径, 以兼容电脑运行脚本
    :param x: 识别起始点 可以使用相对坐标(0-1)或绝对像素值, 可以想象是从屏幕左边拉条线出来, 线左边区域不要去查找
    :param y: 识别起始点 可以使用相对坐标(0-1)或绝对像素值, 可以想象是从屏幕顶部拉条线出来, 线以上区域不要去查找
    :param w: 宽 可以使用相对坐标(0-1)或绝对像素值, 从左边起始初区域延伸多长距离, 如为空, 则查找到屏幕右边
    :param h: 高 可以使用相对坐标(0-1)或绝对像素值, 从顶部起始区域域延伸多长距离, 如为空, 则查找到屏幕底部
    :param threshold:\n
        若 threshold < 0, 则图片保持彩色查找匹配(转换到luv颜色空间), threshold的取值在该范围下无意义;\n
        若 threshold == 0, 对图片进行灰度并反相;\n
        若 threshold > 0, 对图片进行反相并二值化处理(THRESH_BINARY的方式进行二值化), threshold取值范围应为1-255;
    """

    # 如果脚本在电脑上运行, 需要将图片文件提交到手机指定目录
    if not ProjectEnvironment.IMPORT_JAVA_SUCCESS:
        imgs_ = []
        for pi in img:
            imgs_.append(os.path.join(ProjectEnvironment.current_project_dir(), pi))
            if not post_file(pi, os.path.join(ProjectEnvironment.current_project_dir(), os.path.dirname(pi))):
                raise RuntimeError(f"提交文件到手机: {pi} -> {ProjectEnvironment.current_project_dir()}/{pi} 失败☹️")
            if ProjectEnvironment.DEBUG_MODE:
                log_d(f"调试:提交文件到手机: {pi} -> {ProjectEnvironment.current_project_dir()}/{pi} 成功")
    else:
        imgs_ = [__handle_image_path(i) for i in img]
    args = {"templates": ";".join(imgs_), "threshold": threshold}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/screen-find-images", args)


def ui_dump_xml(path=None) -> str:
    """
    [底层接口] 扫描控件布局xml到本地, 一般来说, 在脚本上自行解析xml文件比较复杂, 建议直接使用`ui_match`函数

    :param path: 保存到本地路径
    :returns: 保存的路径
    """
    if path is None:
        path = ProjectEnvironment.DEFAULT_UI_DUMP_PATH
    return engine_api("/uia-dump", {"path": path})


def match_images(template_image: str, prob: float, threshold=0, image=None, x=None, y=None, w=None, h=None) -> \
        [MatchImageResult]:
    """
    对图片在指定范围内进行多次匹配

    :param image: 如image == None, 则进行截图作为识别图片
    :param template_image: 匹配模版
    :param prob: 限制最低相似度, 数字越大, 匹配精确度越高, 数值范围0-1.0
    :param threshold: 图片预处理, 请参考 `screen_find_image`
    """
    args = dict()
    __handle_screen_rect_args(args, x, y, w, h)
    args["threshold"] = threshold
    args["prob"] = prob
    args["template"] = __handle_image_path(template_image)
    if image is not None:
        args["image"] = __handle_image_path(image)
    ret_str = engine_api("/match-images", args)
    result = []
    for line in ret_str.split("\n"):
        if len(line) > 4:
            result.append(EngineResultParser.parse_match_result(line))
    return result


def find_color(base_rgb: str, bias_points: [str] = [], max_fuzzy: int = 3, step_x: int = 5, step_y: int = 5, image=None,
               x=None, y=None, w=None, h=None, max_counts: int = 1) -> [Point]:
    """
    单(多)点找色, 返回匹配颜色的到的坐标

    :param base_rgb: 基点RGB字符串, 格式为R,G,B
    :param bias_points: 偏移点的偏移坐标与RGB字符串
        如果这个数组不为空, 则只匹配基点颜色, 数组的字符串格式为"偏移X,偏移Y|R,G,B", 如["-313,0|243,46,14"], 若格式不当, 将会被忽略!
        如果要使用反色, 即偏移点不为该颜色, 则在RGB颜色前添加~符号 "-313,0|~243,46,14"
    :param max_fuzzy: 找色时颜色相似度的临界值，范围为0 ~ 255（越小越相似，0为颜色相等，255为任何颜色都能匹配）
    :param step_x: 在寻找到一个目标点之后, 应该在横向偏离多少个像素继续寻找
    :param step_y: 在寻找到一个目标点之后, 应该在竖向偏离多少个像素继续寻找
    :param image: image 如image == None, 则进行截图作为识别图片
    :param max_counts: 最大成功匹配坐标点数, 即限制最多返回多少个结果, 可以提高扫描速度
    :return: 找到符合颜色的屏幕坐标点
    """
    args = dict()
    __handle_screen_rect_args(args, x, y, w, h)
    args["rgb"] = base_rgb
    args["prob"] = max_fuzzy
    args["max_counts"] = max_counts
    args["step_x"] = step_x
    args["step_y"] = step_y

    args["points"] = "\n".join(bias_points)
    if image is not None:
        args["image"] = __handle_image_path(image)
    engine_ret = engine_api("/find-color", args)
    if len(engine_ret) == 0:
        return list()
    else:
        result: [] = []
        for line in engine_ret.split("\n"):
            if len(line) > 4:
                result.append(EngineResultParser.parse_point(line))
        return result


def get_color(x: int, y: int, image=None) -> Color:
    """
    获取图片指定坐标的颜色

    :param x: 整数坐标, 应少于等于目标图像的宽
    :param y: 整数坐标, 应少于等于目标图像的高
    :param image: 如image == None, 则进行截图作为识别图片
    :returns: RGB颜色
    """

    args = dict()
    if image is not None:
        args["image"] = __handle_image_path(image)
    args["x"] = x
    args["y"] = y
    return EngineResultParser.parse_color(engine_api("/get-color", args))


def get_multi_color(points: [(int, int)], image=None) -> (Color,):
    """
    获取图片多个坐标的颜色 V80版本新增

    :param points: 如[(100, 255), [45, 588]], 则依次返回坐标100,255以及坐标45, 588的坐标颜色
    :param image: 如image == None, 则进行截图作为识别图片
    :returns: RGB颜色数组
    """
    args = dict()
    if image is not None:
        args["image"] = __handle_image_path(image)
    args["points"] = " ".join([f"{x},{y}" for x, y in points])
    return EngineResultParser.parse_multi_color(engine_api("/get-color", args))


def ensure_kernel_click():
    """
    设置引擎 使用内核点击 重启引擎后生效

    :returns: 当前是否使用内核点击
    """
    return engine_api("/set-no-ra", {"enable": "false"})


def cancel_kernel_click():
    """
    设置引擎 取消内核点击 重启引擎后生效

    :returns: 当前是否使用内核点击
    """
    return engine_api("/set-no-ra", {"enable": "true"})


def pull_file(remote: str, local: str) -> bool:
    """
    在电脑运行脚本上拉取手机对文件到本地

    :param remote: 远程手机文件路径
    :param local: 本地文件路径
    :returns: 是否操作成功
    """
    r = requests.get(f"http://{ProjectEnvironment.DEBUG_IP}:49009/pull-file?path={remote}", stream=True)
    if r.status_code == 200:
        with open(local, 'wb+') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return True
    return False


def post_file(local: str, remote_dir: str = "/sdcard") -> bool:
    """
    在电脑运行脚本上拉取手机对文件到本地

    :param local: 本地文件绝对路径
    :param remote_dir: 远程手机目录, 默认为/sdcard
    :returns: 是否操作成功
    """
    print("参数:", remote_dir, os.path.basename(local))
    f = open(local, mode="rb")
    r = requests.post(f"http://{ProjectEnvironment.DEBUG_IP}:49009/post-file", data={
        "path": remote_dir
    }, files={
        os.path.basename(local): f.read()
    })
    f.close()
    print("提交返回:", r.status_code, r.text)
    return r.status_code < 300
