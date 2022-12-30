from typing import Union
from uiautomator import ExportHandle as EngineApi
from java.util import HashMap
import shutil
import requests
import os
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


def screen_ocr():
    return engine_api("/screen-ocr")


def image_ocr(image_path):
    image_path = image_path if os.path.exists(image_path) else os.path.join(os.getcwd(), image_path)
    return engine_api("/image-ocr", {"path": image_path})


def screen_yolo_locate():
    return engine_api("/key-locate")


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
    if x is not None:
        args["x"] = x
    if w is not None:
        args["w"] = w
    if h is not None:
        args["h"] = h
    if y is not None:
        args["y"] = y
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



