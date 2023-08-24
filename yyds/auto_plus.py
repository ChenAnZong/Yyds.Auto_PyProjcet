from .auto_func import *
from .auto_api_aux import *
import util
import time


class DeviceScreen:
    # 屏幕宽高
    _dw: int = 1080
    _dh: int = 2400

    @classmethod
    def init(cls):
        # 初始化设备参数
        cls._dw, cls._dh = device_get_screen_size()
        util.log_d(f"当前设备: {device_model()} {DeviceScreen._dw}x{DeviceScreen._dh}")

    @classmethod
    def get_screen_wh(cls):
        return cls._dw, cls._dh

    @classmethod
    def get_h(cls):
        return cls._dh

    @classmethod
    def get_w(cls):
        return cls._dw


def download(url, save_local_path) -> bool:
    """
    http网络文件下载
    :param url 下载url
    :param save_local_path 本地保存路径
    :returns: 是否下载成功
    """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(save_local_path, 'wb+') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            return True
    return False


def toast_print(text):
    toast(text)
    util.log_d(text)


def click_target(t: [ResOcr, ResYolo, ResFindImage]):
    click(t.cx, t.cy)


def sleep(t) -> bool:
    util.log_d(f"☢☢☢☢ {t}秒")
    time.sleep(t)
    return True


def false_sleep(t) -> bool:
    sleep(t)
    return False


def random_sleep(a, b):
    return sleep(random.randint(a, b))


def swipe_up():
    swipe(random.randint(int(DeviceScreen._dw * 0.5), int(DeviceScreen._dw * 0.55)),
          random.randint(int(DeviceScreen._dh * 0.75), int(DeviceScreen._dh * 0.8)),
          random.randint(int(DeviceScreen._dw * 0.5), int(DeviceScreen._dw * 0.55)),
          random.randint(int(DeviceScreen._dh * 0.2), int(DeviceScreen._dh * .3)),
          random.randint(1200, 1500))


def swipe_down():
    swipe(random.randint(int(DeviceScreen._dw * 0.4), int(DeviceScreen._dw * 0.6)),
          random.randint(int(DeviceScreen._dh * 0.2), int(DeviceScreen._dh * 0.3)),
          random.randint(int(DeviceScreen._dw * 0.4), int(DeviceScreen._dw * 0.6)),
          random.randint(int(DeviceScreen._dh * 0.75), int(DeviceScreen._dh * 0.9)),
          random.randint(300, 800))


def swipe_right():
    swipe(random.randint(int(DeviceScreen._dw * 0.2), int(DeviceScreen._dw * 0.3)),
          random.randint(int(DeviceScreen._dh * 0.6), int(DeviceScreen._dh * 0.7)),
          random.randint(int(DeviceScreen._dw * 0.75), int(DeviceScreen._dw * 0.9)),
          random.randint(int(DeviceScreen._dh * 0.6), int(DeviceScreen._dh * 0.7)),
          random.randint(200, 600))


def swipe_left():
    swipe(random.randint(int(DeviceScreen._dw * 0.75), int(DeviceScreen._dw * 0.9)),
          random.randint(int(DeviceScreen._dh * 0.6), int(DeviceScreen._dh * 0.7)),
          random.randint(int(DeviceScreen._dw * 0.2), int(DeviceScreen._dw * 0.3)),
          random.randint(int(DeviceScreen._dh * 0.6), int(DeviceScreen._dh * 0.7)),
          random.randint(200, 600))


def swipe_left_top():
    swipe(random.randint(int(DeviceScreen._dw * 0.85), int(DeviceScreen._dw * 0.95)),
          random.randint(int(DeviceScreen._dh * 0.3), int(DeviceScreen._dh * 0.35)),
          random.randint(int(DeviceScreen._dw * 0.1), int(DeviceScreen._dw * 0.2)),
          random.randint(int(DeviceScreen._dh * 0.3), int(DeviceScreen._dh * 0.35)),
          random.randint(200, 600))


def scal_pos_1080_2400(x, y) -> (int, int):
    return int(DeviceScreen._dw * x / 1080), int(DeviceScreen._dh * y / 2400)


def ocr_click_if_found(*text, x=None, y=None, w=None, h=None, offset_h=None, offset_w=None) -> bool:
    """
    如果搜索到所有文字, 点击最后一个
    """
    ocr_result = screen_ocr_x(text, x, y, w, h)
    if len(ocr_result) == len(text):
        r: ResOcr = ocr_result[-1]
        if offset_h is None and offset_w is None:
            click_target(r)
        else:
            x = r.cx
            y = r.cy
            if offset_w is not None:
                x = r.cx + offset_w * r.w
            if offset_h is not None:
                y = r.cy + offset_h * r.h
            click(x, y)
        util.log_d(f"- 完成OCR点击[{r.text}]:", text)
        return True
    else:
        # util.log_d(f"- 未执行OCR点击:", text)
        return False


def ocr_click_any(*text, x=None, y=None, w=None, h=None, offset_h=None, offset_w=None) -> bool:
    """
    如果搜索到任一文字, 点击最后一个
    """
    ocr_result = screen_ocr_x(text, x, y, w, h)
    if len(ocr_result) > 0:
        r: ResOcr = ocr_result[-1]
        if offset_h is None and offset_w is None:
            click_target(r)
        else:
            x = r.cx
            y = r.cy
            if offset_w is not None:
                x = r.cx + offset_w * r.w
            if offset_h is not None:
                y = r.cy + offset_h * r.h
            click(x, y)
        util.log_d(f"- 完成OCR点击[{r.text}]:", text)
        return True
    else:
        # util.log_d(f"- 未执行OCR点击:", text)
        return False


def find_image_click(*img, min_prob=0.5, x=None, y=None, w=None, h=None, offset_x: float = None,
                     offset_y: float = None, threshold: int = -1, wait: int = 0) -> bool:
    r = screen_find_image_x(img, min_prob=min_prob, x=x, y=y, w=w, h=h, threshold=threshold)
    if len(r) == len(img):
        last: ResFindImage = r[-1]
        x = last.cx
        y = last.cy
        if offset_x is not None:
            x = x + DeviceScreen._dw * offset_x
        if offset_y is not None:
            y = y + DeviceScreen._dh * offset_y
        if wait:
            sleep(wait)
        click(x, y)
        util.log_d(f"█ 图片点击 █ {r[-1]} -> {x},{y}")
        return True
    else:
        return False


def ocr_exists_all(*text, x=None, y=None, w=None, h=None) -> bool:
    """

    """
    ocr_result = screen_ocr_x(text, x, y, w, h)
    return len(ocr_result) == len(text)


def ocr_exists_any(*text, x=None, y=None, w=None, h=None) -> bool:
    """

    """
    ocr_result = screen_ocr_x(text, x, y, w, h)
    return len(ocr_result) > 0


def set_text(text):
    x_input_clear()
    sleep(.5)
    x_input_clear()
    sleep(.5)
    x_input_text(text)


def open_app_from_desktop(app_name: str, pkg_name: str, img: str):
    """
    该函数模拟器从手机桌面点开应用
    """
    # 滑回到主页
    do(2, 1.5, False, key_home)
    # 翻动最多4页找到图标
    for _ in range(5):
        sleep(1)
        util.log_d(f"寻找[{app_name}]图标")
        t = screen_find_image_x((img,), min_prob=0.75, threshold=0)
        if t:
            util.log_d("找到图标, 进行点击")
            click_target(t[0])
            sleep(3)
            if device_foreground_package() == pkg_name:
                util.log_d("进入应用成功!")
                return True
        else:
            swipe_left()
    util.log_d(f"进入应用[{app_name}]失败!")
    return False


def exit_go_home():
    toast_print("☃运行时间到了")
    key_home()
    exit(0)


def find_image_click_max_prob(*img, min_prob=0.5, x=None, y=None, w=None, h=None, is_random_click=False,
                              threshold: int = -1) -> bool:
    input_images = []
    must_click = set()
    image_sleep = dict()
    click_time = dict()

    for i in img:
        if isinstance(i, tuple):
            input_images.append(i[0])
            if i[1]:
                must_click.add(i[0])
            if len(i) > 2:
                image_sleep[i[0]] = int(i[2])
            if len(i) > 3:
                click_time[i[0]] = i[3]
        else:
            input_images.append(i)

    r = screen_find_image_x(tuple(input_images), min_prob=min_prob,
                            x=x, y=y, w=w, h=h, threshold=threshold)

    if len(r) > 0:
        sleep(1.5)
        util.log_d("@1再次确认检测目标")
        r = screen_find_image_x(tuple(input_images), min_prob=min_prob,
                                x=x, y=y, w=w, h=h, threshold=threshold)

    if len(r) > 0:
        img_res = list(r)
        if is_random_click:
            random.shuffle(img_res)
        else:
            img_res.sort(key=lambda rf: rf.prob, reverse=True)
        is_found_must_click = False
        for img_res_single in img_res:
            util.log_d(f"█ 返回结果:" + str(img_res_single))
            if img_res_single.name in must_click:
                util.log_d(f"█ 发现必点图片: {img_res_single}")
                if img_res_single.name in image_sleep:
                    sleep(image_sleep[img_res_single.name])
                if img_res_single.name in click_time:
                    for _ in range(click_time[img_res_single.name]):
                        sleep(random.randint(1, 2))
                        click_target(img_res_single)
                else:
                    click_target(img_res_single)
                is_found_must_click = True
        if is_found_must_click:
            return True

        best_img = img_res[0]
        if best_img.name in image_sleep:
            sleep(image_sleep[best_img.name])
        if best_img.name in click_time:
            for _ in range(click_time[best_img.name]):
                sleep(random.randint(1, 2))
                click_target(best_img)
        else:
            click_target(best_img)
        util.log_d(f"█ 最大可能性图片点击 █ {best_img} -> {best_img.cx},{best_img.cy}")
        return True
    else:
        return False
