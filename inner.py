from typing import Union
from uiautomator import ExportHandle as EngineApi
from java.util import HashMap
import shutil
import requests
import os
import random
import re

DEFAULT_SCREEN_SHOT_PATH = "/sdcard/"
DEFAULT_UI_DUMP_PATH = "/data/local/tmp/dump.xml"


def download(url, save_local_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(save_local_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def engine_api(uri: str, options=None):
    if options is None:
        options = {}
    params = HashMap()
    if options:
        for key in options.keys():
            params.put(key, str(options[key]))
    return EngineApi.http(uri, params)


def __handle_screen_rect_args(args: dict, x=None, y=None, w=None, h=None):
    if x is not None:
        args["x"] = x
    if w is not None:
        args["w"] = w
    if h is not None:
        args["h"] = h
    if y is not None:
        args["y"] = y


def toast(content: str):
    """信息提示"""
    engine_api("/toast", {"content": content})


def click(x: Union[str, int, float], y: Union[str, int, float]):
    """点击"""
    engine_api("/touch", {"x": int(x), "y": int(y)})


def swipe(x1, y1, x2, y2, duration):
    engine_api("/swipe", {"x1": int(x1), "x2": int(x2),
                          "y1": int(y1), "y2": int(y2), "duration": int(duration)})


def key_back():
    """返回键"""
    engine_api('/key-code', {"code": "4"})


def key_home():
    """home键"""
    engine_api('/key-code', {"code": "3"})


def key_confirm():
    return engine_api("/key-confirm")


def screenshot(path) -> str:
    """截图"""
    if not path:
        path = DEFAULT_SCREEN_SHOT_PATH
    return engine_api('/screenshot', {"path": path})


def device_get_screen_size() -> (int, int):
    ret = engine_api("/screen-size")
    x, y = ret.split(",")
    return int(x), int(y)


def open_app(pkg):
    return engine_api("/open-app", {"pkg", pkg})


def open_url(url):
    return engine_api("/open-url", {"url", url})


def device_foreground():
    """当前设备信息"""
    result = engine_api('/foreground')
    # if result:
    #     current_package_name, current_activity, pid = result.split(" ")
    return result.split(" ")


def device_code():
    return engine_api("/imei")


def screen_ocr(x=None, y=None, w=None, h=None, use_gpu=True):
    args = {"use_gpu": "true" if use_gpu else "false"}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/screen-ocr", args)


def image_ocr(image_path):
    image_path = image_path if os.path.exists(image_path) else os.path.join(os.getcwd(), image_path)
    return engine_api("/image-ocr", {"path": image_path})


def screen_yolo_locate(x=None, y=None, w=None, h=None, use_gpu=True):
    args = {"use_gpu": "true" if use_gpu else "false"}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/key-locate", args)


def model_yolo_reload(ncnn_bin_path, ncnn_param_path):
    """
    自定义你的yolo模型, 需要转换为ncnn模型
    """
    engine_api("/set-yolo-model", {
        "bin_file_path": ncnn_bin_path,
        "param_file_path": ncnn_param_path
    })


def screen_find_image(*img, x=None, y=None, w=None, h=None):
    """
    同时寻找多张图片, 可以指定范围
    """
    imgs_ = [i if os.path.exists(i) else os.path.join(os.getcwd(), i) for i in img]
    args = {"templates": ";".join(imgs_)}
    __handle_screen_rect_args(args, x, y, w, h)
    return engine_api("/screen-find-images", args)


def ui_match(match_from_cache=False, **match_params):
    params_ = {"match_from_cache": "true" if match_from_cache else "false"}
    for k in match_params.keys():
        if k == "class_":
            params_["class"] = match_params[k]
        else:
            params_[str(k).replace("_", "-")] = match_params[k]
    return engine_api("/uia-match", params_)


def ui_exist(match_from_cache=False, **match_params):
    params_ = {"match_from_cache": "true" if match_from_cache else "false"}
    match_params["limit"] = 1
    for k in match_params.keys():
        if k == "class_":
            params_["class"] = match_params[k]
        else:
            params_[str(k).replace("_", "-")] = match_params[k]
    return engine_api("/uia-match", params_)


def ui_dump_xml(path):
    if path is None:
        path = DEFAULT_UI_DUMP_PATH
    return engine_api("/uia-dump", {"path": path})


def shell(*cmd):
    """
    执行shell脚本, 返回shell字符串
    """
    return engine_api("/shell", {"cmd": ";".join(cmd)})


def _version():
    """插件版本号"""
    return engine_api("/version")


def _pid():
    return engine_api("/pid")


def _uid():
    return engine_api("/uid")


def _ping():
    return engine_api("/ping")


def _reboot():
    return engine_api("/reboot")


def _exit():
    return engine_api("/exit")


def _press_down(x, y):
    return engine_api("/press_down", {"x": x, "y": y})


def _press_up(x, y):
    return engine_api("/press_up", {"x": x, "y": y})


def _press_move(x, y):
    return engine_api("/press_move", {"x": x, "y": y})


# -----------------
from typing import Union, List


PROJECT_DIR = "/sdcard/Yyds.Py/test"


# 请求查找图片
class RequestFindImage:
    name: str
    path: str
    prob: float

    def __init__(self, name: str, path: str, prob: float):
        self.name = name
        self.path = path
        self.prob = prob

    def __repr__(self):
        return '{{ name="{}",path="{}",prob={}}}'.format(self.name, self.path, self.prob)


# 返回查找到的图片
class ResFindImage:
    name: str
    path: str
    prob: float
    width: int
    height: int
    x: int
    y: int

    def __init__(self, name: str, path: str, prob: float, width: int, height: int, x: int, y: int):
        self.name = name
        self.path = path
        self.prob = prob
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def __repr__(self):
        return '{{name="{}",path="{}",prob={},width={},height={},x={},y={}}}'.format(self.name, self.path, self.prob,
                                                                                     self.width, self.height, self.x,
                                                                                     self.y)


# yolo返回
class ResYolo:
    label: str
    cx: int
    cy: int
    x: float
    y: float
    w: float
    h: float
    prob: float

    def __init__(self, label: str, cx: int, cy: int, x: float, y: float, w: float, h: float, prob: float):
        self.label = label
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.prob = prob

    def __repr__(self):
        return '{{label="{}",cx={},cy={},x={},y={},w={},h={},prob={}}}'.format(self.label, self.cx, self.cy, self.x,
                                                                               self.y, self.w, self.h, self.prob)


class ResOcr:
    prob: float
    text: str
    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float
    x4: float
    y4: float

    def __init__(self, prob: float, text: str, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float,
                 x4: float, y4: float):
        self.prob = prob
        self.text = text
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4

    def __repr__(self):
        return '{{ prob={},text="{}",x1={},y1={},x2={},y2={},x3={},y3={},x4={},y4={} }}'.format(self.prob, self.text,
                                                                                                self.x1, self.y1,
                                                                                                self.x2, self.y2,
                                                                                                self.x3, self.y3,
                                                                                                self.x4, self.y4)


# 获取资源完整路径
def res(res_path: str):
    global PROJECT_DIR
    return '{}/{}'.format(PROJECT_DIR, res_path.replace('./', ''))


# 查找图片
def yy_find_image(fd_images: List[Union[str, RequestFindImage]], prob: float = 0.9) -> List[ResFindImage]:
    in_list: List[RequestFindImage] = list()
    for fd in fd_images:
        if type(fd) is str:
            in_list.append(RequestFindImage(fd, fd, prob))
        elif type(fd) is RequestFindImage:
            if fd.prob == 0:
                fd.prob = prob
            in_list.append(fd)

    fd_paths: List[str] = list()
    for it in in_list:
        fd_paths.append(it.path)
    str_fds: str = screen_find_image(";".join(fd_paths))
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
            if fd_image.prob >= it.prob:
                results.append(fd_image)
            index = index + 1
    return results


# 查找第一张图片
def yy_find_image_first(fd_images: List[Union[str, RequestFindImage]], prob: float = 0.9) -> Union[ResFindImage, None]:
    find_images = yy_find_image(fd_images, prob)
    if len(find_images) > 0:
        return find_images[0]
    return None


def yy_yolo_find(labels=None, prob: float = 0.9) -> List[ResYolo]:
    if labels is None:
        labels = []
    str_fds = screen_yolo_locate()
    sp_fds = str_fds.split('\n')
    results: List[ResYolo] = list()
    for fd in sp_fds:
        if fd != "":
            result = re.match(
                r'{label=\'(.*)\', cx=(\d+), cy=(\d+), x=(\d+.\d+), y=(\d+.\d+), w=(\d+.\d+), h=(\d+.\d+), prob=(\d+.\d+)}',
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
            if res_yolo.prob >= prob:
                if len(labels) > 0:
                    for it in labels:
                        if re.match(it, res_yolo.label):
                            results.append(res_yolo)
                else:
                    results.append(res_yolo)
    return results


# 查找第一个yolo
def yy_yolo_find_first(labels=None, prob: float = 0.9) -> Union[ResYolo, None]:
    if labels is None:
        labels = []
    find_yolos = yy_yolo_find(labels, prob)
    if len(find_yolos) > 0:
        return find_yolos[0]
    return None


# 随机click
def random_click(x: int, y: int, w: int, h: int):
    x = x
    y = y
    y += h * 0.25 + random.uniform(h * 0.25, h * 0.75)
    x += w * 0.25 + random.uniform(w * 0.25, w * 0.75)
    click(x, y)


def find_ocr(texts=None) -> List[ResOcr]:
    if texts is None:
        texts = []
    fd_ocr_str: str = screen_ocr()
    fd_sp = fd_ocr_str.split('\n')
    results: List[ResOcr] = list()
    for fd in fd_sp:
        if fd != "":
            prob, text, pos_split = fd.split('\t')
            result = re.match(r'(\d+),(\d+) (\d+),(\d+) (\d+),(\d+) (\d+),(\d+)', pos_split).groups()
            res = ResOcr(prob, text, result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                         result[7])
            if len(texts) > 0:
                for it in texts:
                    if re.match(it, res.text):
                        results.append(res)
            else:
                results.append(res)
    return results


# 查找第一个findOcr
def find_ocr_first(texts=None) -> Union[ResYolo, None]:
    if texts is None:
        texts = []
    find_ocrs = find_ocr(texts)
    if len(find_ocrs) > 0:
        return find_ocrs[0]
    return None
