"""
@author  玩机达人 微信:wjzy_yyds
@desc    Yyds.Auto 官方封装Python函数 更多用法 https://yydsxx.com
@tip     _x结尾系列为高级封装函数; _开头为内部函数, 一般不对外使用
@version (30) 3.50
"""
import json
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

try:
    from uiautomator import ExportHandle as EngineApi
    from java.util import HashMap
except:
    print(traceback.format_exc(), file=sys.stderr)

PROJECT_DIR = "/sdcard/Yyds.Py/test"

DEFAULT_SCREEN_SHOT_PATH = "/sdcard/"
DEFAULT_UI_DUMP_PATH = "/data/local/tmp/dump.xml"
DEBUG_MODE = True


def random_click(x: int, y: int, w: int, h: int):
    """
    在指定区域内 随机click
    """
    x = x
    y = y
    y += h * 0.25 + random.uniform(h * 0.25, h * 0.75)
    x += w * 0.25 + random.uniform(w * 0.25, w * 0.75)
    click(x, y)


def md5_file(path):
    """
    计算文件md5
    :param path 文件路径
    """
    md5 = hashlib.md5()
    f = open(path, mode="rb")
    md5.update(f.read())
    f.close()
    md5_sum = md5.hexdigest()
    return md5_sum


def md5_str(text):
    """
    计算文本md5
    :param text 文本内容
    :returns 文本md5
    """
    md5 = hashlib.md5()
    md5.update(text.encode("utf-8"))
    md5_sum = md5.hexdigest()
    return md5_sum


def download(url, save_local_path):
    """
    http网络文件下载
    :param url 下载url
    :param save_local_path 本地保存路径
    """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(save_local_path, 'wb+') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def engine_api(uri: str, options=None):
    """
    自动化引擎底层RPC调用java层接口
    :param uri 远程接口
    :param options 参数，字典类型，所有键值都应为str类型
    """
    if options is None:
        options = {}
    if options is None:
        options = {}
    params = HashMap()
    if options:
        for key in options.keys():
            params.put(key, str(options[key]))
    ret = EngineApi.http(uri, params)
    if DEBUG_MODE:
        print(uri, ret)
    return ret


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


def toast(content: str):
    """
    信息提示
    需要打开 应用 后台窗口弹出权限
    """
    engine_api("/toast", {"content": content})


def click(x: Union[str, int], y: Union[str, int]):
    """
    点击坐标点
    :param x 屏幕绝对坐标，不支持小数
    :param y 屏幕绝对坐标，不支持小数
    """
    engine_api("/touch", {"x": int(x), "y": int(y)})


def click_double(x: Union[str, int], y: Union[str, int]):
    """
    双击坐标点
    """
    click(x, y)
    time.sleep(290)
    click(x, y)


def swipe(x1, y1, x2, y2, duration):
    """
    滑动
    :param x1 起始坐标 x
    :param y1 起始坐标 y
    :param x2 目标坐标 x
    :param y2 目标坐标 y
    :param duration 滑动耗时（毫秒） 越小滑动越快
    """
    engine_api("/swipe", {"x1": int(x1), "x2": int(x2),
                          "y1": int(y1), "y2": int(y2), "duration": int(duration)})


def key_back():
    """
    注入返回键
    """
    engine_api('/key-code', {"code": "4"})


def key_home():
    """
    注入home键
    """
    engine_api('/key-code', {"code": "3"})


def key_confirm():
    """
    确认键，一般用于编辑框确实搜索，确认提交
    """
    return engine_api("/key-confirm")


def key_code(code):
    """
    注入键值码, 键值码数值, 请参考文档博客文章
    @param code 键值码
    """
    return engine_api("/key-code", {"code", int(code)})


def screenshot(path=None) -> str:
    """
    截图
    :param path 截图保存路径, 此接口无需申请任何权限
    """
    if not path:
        path = DEFAULT_SCREEN_SHOT_PATH
    return engine_api('/screenshot', {"path": path})


def device_get_screen_size() -> (int, int):
    """
    获取屏幕分辨率大小
    :returns 宽, 高
    """
    ret = engine_api("/screen-size")
    x, y = ret.split(",")
    return int(x), int(y)


def open_app(pkg):
    """
    根据包名打开app
    """
    return engine_api("/open-app", {"pkg", pkg})


def open_url(url):
    """
    打开系统u rl
    如果 url为 http 链接, 即使用系统默认的浏览器应用
    也能打开其它系统链接 比如电话tel:21113336
    成功返回:Starting: Intent { act=android.intent.action.VIEW dat=tel:xxxxxxxxxx }
    错误返回:Starting: Intent { act=android.intent.action.VIEW dat=asdfs }
Error: Activity not started, unable to resolve Intent { act=android.intent.action.VIEW dat=asdfs flg=0x10000000 }
    """
    return engine_api("/open-url", {"url", url})


def ensure_kernel_click():
    """
    设置引擎 使用内核点击 后面都生效
    :returns 当前是否使用内核点击
    """
    return engine_api("/set-no-ra", {"enable": "false"})


def cancel_kernel_click():
    """
    设置引擎 取消内核点击
    :returns: 当前是否使用内核点击
    """
    return engine_api("/set-no-ra", {"enable": "true"})


class DeviceForegroundResponse:
    def __init__(self, package: str, activity: str, pid: int):
        self.package = package
        self.activity_name = activity
        self.pid = pid

    @property
    def full_activity_name(self):
        if self.activity_name.startswith("."):
            return self.activity_name
        else:
            return self.package + self.activity_name

    def __repr__(self):
        return 'DeviceForegroundResponse {{ package="{}", activity="{}", pid={} }}'.format(self.package, self.activity_name, self.pid)


def device_foreground() -> Optional[DeviceForegroundResponse]:
    """
    当前设备信息
    :returns: 当前包名, 当前应用Activity名(有时相对, 有时绝对取决于应用), 应用进程pid
    """
    result = engine_api('/foreground')
    s = result.split(" ")
    if len(s) < 2:
        return None
    return DeviceForegroundResponse(result[0], result[1], result[2])


def is_in_app(pkg:str) -> bool:
    """
    @ 当前是否在某应用界面内
    :param pkg 应用包名
    """
    return pkg == device_foreground().package


def device_code():
    """
    应用imei码, 可作为应用唯一硬件码, 提醒:在root下此码可被轻易篡改返回结果
    :returns: str
    """
    return engine_api("/imei")


def device_model() -> str:
    """
    当前手机型号
    """
    return shell("getprop ro.product.model")


def is_net_online():
    """
    通过请求指定链接测试当前网络是否畅通
    """
    return engine_api("/is-net-online") == "true"


def screen_ocr(x=None, y=None, w=None, h=None, use_gpu=False):
    """
    使用引擎识别当前屏幕的文字, 可指定识别范围
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽
    :param h: 高
    :param use_gpu: 是否使用Gpu运算, 性能差的手机不建议, 会导致手机掉帧
    :returns: 引擎返回识别文本
    """
    args = {"use_gpu": "true" if use_gpu else "false"}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/screen-ocr", args)


def image_ocr(image_path: str, x=None, y=None, w=None, h=None, use_gpu=True):
    """
    使用引擎识别指定图片文字, 可指定识别范围
    :param image_path 图片的绝对路径
    :param x 识别起始点 可以使用相对坐标(0-1)
    :param y 识别起始点 可以使用相对坐标(0-1)
    :param w 宽 可以使用相对坐标(0-1)
    :param h 高 可以使用相对坐标(0-1)
    :param use_gpu 是否使用Gpu运算, 性能差的手机不建议, 会导致手机掉帧
    """
    image_path = image_path if os.path.exists(image_path) else os.path.join(os.getcwd(), image_path)
    args = {"path": image_path, "use_gpu": "true" if use_gpu else "false"}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/image-ocr", args)


def screen_yolo_locate(x=None, y=None, w=None, h=None, use_gpu=True):
    """
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param use_gpu 是否使用gpu运行，建议处理器较差的机器不要使用gpu运算，会卡顿
    :returns: 引擎返回识别文本
    """
    args = {"use_gpu": "true" if use_gpu else "false"}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/key-locate", args)


def model_yolo_reload(ncnn_bin_path, ncnn_param_path):
    """
    自定义你的yolo模型, 需要转换为ncnn模型
    默认加载 /data/local/tmp/yyds.bin
    默认加载 /data/local/tmp/yyds.param
    """
    engine_api("/set-yolo-model", {
        "bin_file_path": ncnn_bin_path,
        "param_file_path": ncnn_param_path
    })


def model_ocr_reload(ncnn_bin_path, ncnn_param_path):
    """
    自定义你的pp ocr模型, 需要转换为ncnn模型
    引擎内置OCR模型, 一般不用自己训练
    """
    engine_api("/set-ocr-model", {
        "bin_file_path": ncnn_bin_path,
        "param_file_path": ncnn_param_path
    })


def screen_find_image(*img, x=None, y=None, w=None, h=None):
    """
    在屏幕上同时寻找多张图片, 可以指定范围
    :param img 图片路径, 如果传入的是相对路径, 则会被处理成绝对路径
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    """
    imgs_ = [os.path.join(os.getcwd(), i) if os.path.exists(os.path.join(os.getcwd(), i)) else i for i in img]
    args = {"templates": ";".join(imgs_)}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/screen-find-images", args)


class Node:
    """
    控件元素
    """
    def __init__(self, node_obj: dict):
        self.bound_str: str = node_obj.get("boundsString")
        self.child_count: int = node_obj.get("childCount")
        self.parent_count: int = node_obj.get("parentCount")
        self.class_name: str = node_obj.get("cls")
        self.pkg: str = node_obj.get("pkg")
        self.text: str = node_obj.get("text")
        self.desc: str = node_obj.get("desc")
        self.id: str = node_obj.get("id")
        self.index: int = int(node_obj.get("index"))
        self.is_check_able: bool = node_obj.get("isCheckable")
        self.is_clicked: bool = node_obj.get("isChecked")
        self.is_enable: bool = node_obj.get("isEnable")
        self.is_foucuable: bool = node_obj.get("isFocusable")
        self.is_foucesed: bool = node_obj.get("isFocused")
        self.is_long_click_able: bool = node_obj.get("isLongClickable")
        self.is_password: bool = node_obj.get("isPassword")
        self.is_scroll_able: bool = node_obj.get("isScrollable")
        self.is_selected: bool = node_obj.get("isSelected")
        self.is_visible: bool = node_obj.get("isVisible")

    def __str__(self):
        return f"Node {{ class_name:{self.class_name}, bound_str:{self.bound_str}, child_count:{self.child_count}, " \
               f"parent_count:{self.parent_count}, pkg:{self.pkg}, text:{self.text}, desc:{self.desc}, id:{self.id}" \
               f"index: {self.index} click_able: {self.is_clicked} long_click_able: {self.is_long_click_able} " \
               f"is_scroll_able: {self.is_scroll_able} }}"

    def __repr__(self):
        return self.__str__()


def ui_match(match_from_cache=False, **match_params) -> List[Node]:
    """
    当前屏幕ui控件定位
    :param match_from_cache 是否从最后一次dump的缓存中匹配 可以加快搜索速度
    :return 识别结果
    """
    params_ = {"match_from_cache": "true" if match_from_cache else "false"}
    for k in match_params.keys():
        if k == "class_":
            params_["class"] = match_params[k]
        else:
            params_[str(k).replace("_", "-")] = match_params[k]
    ret_str = engine_api("/uia-match", params_)
    return [Node(i) for i in json.loads(ret_str)]


def ui_exist(match_from_cache=False, **match_params) -> bool:
    """
    ui 是否存在
    :returns bool ui是否存在
    """
    params_ = {"match_from_cache": "true" if match_from_cache else "false"}
    match_params["limit"] = 1
    for k in match_params.keys():
        if k == "class_":
            params_["class"] = match_params[k]
        else:
            params_[str(k).replace("_", "-")] = match_params[k]
    return len(engine_api("/uia-match", params_)) > 1


def ui_dump_xml(path):
    """
    扫描控件布局xml到本地
    :param path 保存到本地路径
    """
    if path is None:
        path = DEFAULT_UI_DUMP_PATH
    return engine_api("/uia-dump", {"path": path})


def shell(*cmd):
    """
    自动化引擎 执行shell脚本, 返回shell字符串, 可执行多条
    :return 返回shell执行输出 包括错误流!
    """
    return engine_api("/shell", {"cmd": ";".join(cmd)})


def _version():
    """
    自动化引擎 插件版本号, 即插件应用的app VersionCode
    """
    return engine_api("/version")


def _pid():
    """
    自动化引擎 [调试使用] 自动化引擎进程pid
    """
    return engine_api("/pid")


def _uid():
    """
    自动化引擎 [调试使用] 自动化引擎进程uid
    """
    return engine_api("/uid")


def _ping() -> bool:
    """
    自动化引擎 [调试使用] 插件自动化引擎rpc通讯检测
    :returns bool 是否通讯成功
    """
    return engine_api("/ping") == "pong"


def _reboot():
    """
    自动化引擎 [调试使用] 重启自动化引擎
    """
    return engine_api("/reboot")


def _exit():
    """
    自动化引擎 [调试使用] 结束自动化
    """
    return engine_api("/exit")


def _press_down(x, y):
    """
    自动化引擎 模式单个手指按下坐标
    """
    return engine_api("/press_down", {"x": x, "y": y})


def _press_up(x, y):
    """
    自动化引擎 模式单个手指弹起坐标
    """
    return engine_api("/press_up", {"x": x, "y": y})


def _press_move(x, y):
    """
    自动化引擎 模式单个手指按住移动手指
    """
    return engine_api("/press_move", {"x": x, "y": y})


def _reload_py_module(module_name):
    """
    指定重新加载某模块
    @param module_name 模块名
    """
    importlib.reload(sys.modules[module_name])


class RequestFindImage:
    """
    自动化引擎 查找图片请求参数
    """

    def __init__(self, name: str, path: str, min_prob: float):
        self.name = name    # 传入的图片参数
        self.path = path    # 传入的图片路径
        self.min_prob = min_prob    # 要求最低置信率

    def __str__(self):
        return 'RequestFindImage {{ name="{}", path="{}", min_prob={} }}'.format(self.name, self.path, self.min_prob)

    def __repr__(self):
        return str(self)


class ResFindImage:
    """
    自动化引擎 封装高级查找图片(模版匹配算法)请求参数 所有坐标均为屏幕绝对坐标
    """

    def __init__(self, name: str, path: str, prob: float, width: int, height: int, x: int, y: int):
        self.name = name    # 传入目标的图片路径参数
        self.path = path    # 传入目标的图片路径
        self.min_prob = prob    # 要求最低置信率
        self.width = width      # 匹配到的图片宽(浮点运算原因, 可能与传入图片的宽相差1像素)
        self.height = height    # 匹配到的图片高(浮点运算原因, 可能与传入图片的高相差1像素)
        self.x = x              # 左上角 x
        self.y = y              # 左上角 y

    def __str__(self):
        return f'ResFindImage {{ name=f"{self.name}", path=f"{self.path}", prob={self.min_prob}, width={self.width}, ' \
               f'height={self.height}, x={self.x}, y={self.y} }}'

    def __repr__(self):
        return str(self)


class ResYolo:
    """
    自动化引擎 封装高级查找图片(Yolo ai算法)返回结果, 所有坐标均为屏幕绝对坐标
    """

    def __init__(self, label: str, cx: int, cy: int, x: float, y: float, w: float, h: float, prob: float):
        self.label = label
        self.cx = cx  # 中间 x
        self.cy = cy  # 中间 y
        self.x = x  # 左上角 x
        self.y = y  # 左上角 y
        self.w = w  # 宽
        self.h = h  # 高
        self.prob = prob  # yolo 识别置信率

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'ResYolo {{label="{}", cx={}, cy={}, x={}, y={}, w={}, h={}, prob={} }}'.format(self.label, self.cx,
                                                                                            self.cy, self.x,
                                                                                            self.y, self.w, self.h,
                                                                                            self.prob)


class ResOcr:
    """
    自动化引擎 封装OCR识别返回结果, 所有坐标均为绝对坐标
    :param x1
    """

    def __init__(self, prob: float, text: str, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int,
                 x4: int, y4: int):
        self.prob = prob  # OCR识别置信率
        self.text = text  # OCR识别文本
        self.x1 = x1  # 左上x
        self.y1 = y1  # 左上y
        self.x2 = x2  # 右上x
        self.y2 = y2  # 右上y

        self.x3 = x3  # 右下x
        self.y3 = y3  # 右下y
        self.x4 = x4  # 左下x
        self.y4 = y4  # 左下y

    # 中间 x
    @property
    def cx(self):
        """
        中间 x
        """
        return int((self.x1 + self.x3) / 2)

    @property
    def cy(self):
        """
        中间 y
        """
        return int((self.y1 + self.y3) / 2)

    def __str__(self):
        return 'ResOcr# {{ prob={}, text="{}", x1={}, y1={}, x2={}, y2={}, x3={}, y3={}, x4={}, y4={} }}' \
            .format(self.prob, self.text, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4)

    def __repr__(self):
        return self.__str__()


def screen_find_image_x(fd_images: Union[Tuple[str, ...], Tuple[RequestFindImage, ...]],
                        min_prob: float = 0.5, x=None, y=None, w=None, h=None) \
        -> Tuple[ResFindImage]:
    """
    查看图片
    :param fd_images 需要查找的图片
    :param min_prob  float 最低置信率
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    """
    in_list: List[RequestFindImage] = list()
    for fd in fd_images:
        if type(fd) is str:
            in_list.append(RequestFindImage(fd, fd, min_prob))
        elif type(fd) is RequestFindImage:
            if fd.prob == 0:
                fd.prob = min_prob
            in_list.append(fd)

    fd_paths: List[str] = list()
    for it in in_list:
        fd_paths.append(it.path)
    str_fds: str = screen_find_image(*fd_paths, x=x, y=y, w=w, h=h)
    sp_fds = str_fds.split('\n')
    results: List[ResFindImage] = list()
    index = 0
    for fd in sp_fds:
        if fd != "":
            it = in_list[index]
            result = re.match(r'(.*)\t(\d+.\d+) (\d+),(\d+) (\d+),(\d+)', fd).groups()
            fd_image = ResFindImage(
                it.name,
                result[0],
                float(result[1]),
                int(result[2]),
                int(result[3]),
                int(result[4]),
                int(result[5])
            )
            if fd_image.min_prob >= it.min_prob:
                results.append(fd_image)
            index = index + 1
    return tuple(results)


def screen_find_image_first_x(fd_images: Tuple[Union[str, RequestFindImage]], min_prob: float = 0.9,
                              x=None, y=None, w=None, h=None) -> Union[ResFindImage, None]:
    """
    # 屏幕查找图片, 仅返回第一张查找结果

    :param fd_images 需要查找的图片
    :param min_prob  最低置信率
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    """
    find_images = screen_find_image_x(*fd_images, min_prob=min_prob, x=x, y=y, w=w, h=h)
    if len(find_images) > 0:
        return find_images[0]
    return None


def screen_yolo_find_x(specify_labels=None, min_prob: float = 0.9, x=None, y=None, w=None, h=None, use_gpu=False) \
        -> Tuple[ResYolo]:
    """
    通过yolo算法识别当前屏幕内容
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param use_gpu: 是否使用Gpu运算, 性能差的手机不建议, 会导致手机掉帧
    :param specify_labels: 是否寻找指定label内容
    :param min_prob:       最低置信率
    :param use_gpu:        是否使用gpu运算
    :returns: 识别结果列表
    """
    if specify_labels is None:
        specify_labels = []
    str_fds = screen_yolo_locate(use_gpu=use_gpu, x=x, y=y, w=w, h=h)
    sp_fds = str_fds.split('\n')
    # print("解析" + str(sp_fds))
    results: List[ResYolo] = list()
    for fd in sp_fds:
        if fd != "":
            result = re.match(
                r'{label=\'(.*)\', cx=(\d+), cy=(\d+), x=(\d+.\d+), y=(\d+.\d+), w=(\d+.\d+), h=(\d+.\d+), '
                r'prob=(\d+.\d+)}',
                fd).groups()
            res_yolo = ResYolo(
                result[0],
                int(result[1]),
                int(result[2]),
                float(result[3]),
                float(result[4]),
                float(result[5]),
                float(result[6]),
                float(result[7]),
            )
            if res_yolo.prob >= min_prob:
                if len(specify_labels) > 0:
                    for it in specify_labels:
                        if re.match(it, res_yolo.label):
                            results.append(res_yolo)
                else:
                    results.append(res_yolo)
    return tuple(results)


def screen_yolo_find_first_x(labels=None, prob: float = 0.9, x=None, y=None, w=None, h=None, use_gpu=False) \
        -> Union[ResYolo, None]:
    """
    :returns :略, 请参考yolo_find_x, 返回第一个结果
    """
    if labels is None:
        labels = []
    if isinstance(labels, str):
        labels = (labels,)
    find_yolo_results = screen_yolo_find_x(labels, prob, x=x, y=y, w=w, h=h, use_gpu=use_gpu)
    if len(find_yolo_results) > 0:
        return find_yolo_results[0]
    return None


def screen_ocr_x(specific_texts: Union[list, tuple] = None, x=None, y=None, w=None, h=None, use_gpu=False) \
        -> Tuple[ResOcr]:
    """
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param use_gpu: 是否使用Gpu运算, 性能差的手机不建议, 会导致手机掉帧
    :param specific_texts 指定查找文本, 若未指定, 则返回整个屏幕的ocr结果, 支持python正则
    """
    if isinstance(specific_texts, str):
        specific_texts = (specific_texts,)
    if specific_texts is None:
        specific_texts = []
    fd_ocr_str: str = screen_ocr(x=x, y=y, w=w, h=h, use_gpu=use_gpu)
    fd_sp = fd_ocr_str.split('\n')
    results: List[ResOcr] = list()
    for fd in fd_sp:
        if fd != "":
            prob, text, pos_split = fd.split('\t')
            result = re.match(r'(\d+),(\d+) (\d+),(\d+) (\d+),(\d+) (\d+),(\d+)', pos_split).groups()
            res = ResOcr(prob, text, int(result[0]), int(result[1]), int(result[2]), int(result[3]),
                         int(result[4]), int(result[5]), int(result[6]), int(result[7]))
            if len(specific_texts) > 0:
                for it in specific_texts:
                    if re.match(it, res.text):
                        results.append(res)
            else:
                results.append(res)
    return tuple(results)


def screen_ocr_first_x(specific_texts=Union[list, tuple], x=None, y=None, w=None, h=None, use_gpu=False) \
        -> Union[ResOcr, None]:
    """
    :returns :略, 请参考screen_ocr_x , 返回第一个结果
    """
    if specific_texts is None:
        specific_texts = []
    if isinstance(specific_texts, str):
        specific_texts = (specific_texts,)
    find_ocr_results = screen_ocr_x(specific_texts, x=x, y=y, w=w, h=h, use_gpu=use_gpu)
    if len(find_ocr_results) > 0:
        return find_ocr_results[0]
    return None


def paste(text: str):
    """
    粘贴文本, 支持输入中文, 需要目标应用读写粘贴板权限
    目前存在一定兼容性, 请使用 input_text
    """
    return engine_api("/paste", {"text": str(text)})


def input_text(text: str) -> int:
    """
    注入文本, 安卓系统限制, 不支持中文
    """
    return int(engine_api("/inject-text", {"text": str(text)}))
