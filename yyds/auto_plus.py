from .auto_func import *
from .auto_api_aux import *
from .util import *
import time


class DeviceScreen:
    # 屏幕宽高
    _dw: int = 1080
    _dh: int = 2400

    @classmethod
    def init(cls):
        # 初始化设备参数
        cls._dw, cls._dh = device_get_screen_size()
        log_d(f"当前设备: {device_model()} {DeviceScreen._dw}x{DeviceScreen._dh}")

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
    http网络文件下载, 请确保URL可访问

    :param url: 下载url
    :param save_local_path: 本地保存路径
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
    """
    对指定文本打印到日志并弹出toast

    :param text: 需要提示并打印的文本
    :return: 无
    """
    toast(text)
    log_d(text)


def click_target(t: [ResOcr, ResYolo, ResFindImage]):
    """
    点击对象

    :param t: 点击对象, 可为OCR识别结果，Yolo识别识别, 找图结果
    :return: 无
    """
    click(t.cx, t.cy)


def sleep(t) -> bool:
    """
    暂停代码运行指定秒数

    :param t: 暂停秒数, 可以为小数, 如0.1或者.1即为10分之一秒
    :return: 无
    """
    log_d(f"☢☢☢☢ {t}秒")
    time.sleep(t)
    return True


def false_sleep(t: Union[int, float]) -> bool:
    """
    暂停代码运行指定秒数 并返回假

    :param t: 暂停秒数, 可以为小数, 如0.1或者.1即为10分之一秒
    :return: 无
    """
    sleep(t)
    return False


def random_sleep(a:int, b:int):
    """
    暂停代码运行指定秒数 并返回假

    :param a: 区间开始,
    :param b: 区间结束
    :return:
    """
    return sleep(random.randint(a, b))


def swipe_up():
    """
    往上滑动

    :return: 无
    """
    swipe(random.randint(int(DeviceScreen._dw * 0.5), int(DeviceScreen._dw * 0.55)),
          random.randint(int(DeviceScreen._dh * 0.75), int(DeviceScreen._dh * 0.8)),
          random.randint(int(DeviceScreen._dw * 0.5), int(DeviceScreen._dw * 0.55)),
          random.randint(int(DeviceScreen._dh * 0.2), int(DeviceScreen._dh * .3)),
          random.randint(1200, 1500))


def swipe_down():
    """
    往下滑动

    :return: 无
    """
    swipe(random.randint(int(DeviceScreen._dw * 0.4), int(DeviceScreen._dw * 0.6)),
          random.randint(int(DeviceScreen._dh * 0.2), int(DeviceScreen._dh * 0.3)),
          random.randint(int(DeviceScreen._dw * 0.4), int(DeviceScreen._dw * 0.6)),
          random.randint(int(DeviceScreen._dh * 0.75), int(DeviceScreen._dh * 0.9)),
          random.randint(300, 800))


def swipe_right():
    """
    往右滑动

    :return: 无
    """
    swipe(random.randint(int(DeviceScreen._dw * 0.2), int(DeviceScreen._dw * 0.3)),
          random.randint(int(DeviceScreen._dh * 0.6), int(DeviceScreen._dh * 0.7)),
          random.randint(int(DeviceScreen._dw * 0.75), int(DeviceScreen._dw * 0.9)),
          random.randint(int(DeviceScreen._dh * 0.6), int(DeviceScreen._dh * 0.7)),
          random.randint(200, 600))


def swipe_left():
    """
    往左滑动

    :return: 无
    """
    swipe(random.randint(int(DeviceScreen._dw * 0.75), int(DeviceScreen._dw * 0.9)),
          random.randint(int(DeviceScreen._dh * 0.6), int(DeviceScreen._dh * 0.7)),
          random.randint(int(DeviceScreen._dw * 0.2), int(DeviceScreen._dw * 0.3)),
          random.randint(int(DeviceScreen._dh * 0.6), int(DeviceScreen._dh * 0.7)),
          random.randint(200, 600))


def scal_pos_1080_2400(x, y) -> (int, int):
    """
    进行全分辨率适配, 按比例对屏幕坐标进行转换

    :param x: x
    :param y: y
    :return: 坐标
    """
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
        log_d(f"- 完成OCR点击[{r.text}]:", text)
        return True
    else:
        # log_d(f"- 未执行OCR点击:", text)
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
        log_d(f"- 完成OCR点击[{r.text}]:", text)
        return True
    else:
        # log_d(f"- 未执行OCR点击:", text)
        return False


def find_image_click(*img, min_prob=0.5, x=None, y=None, w=None, h=None, offset_x: float = None,
                     offset_y: float = None, threshold: int = -1, wait: int = 0) -> bool:
    """
    若找到了所有图片, 则点击最后一张图片, 可以传入点击偏移
    
    :param img: 图片字符串或者元祖(图片, 是否必须点击, 点击前停顿秒数, 点击次数)
    :param min_prob: 过滤置信率
    :param x: 指定范围, 参考找图函数
    :param y: 指定范围, 参考找图函数
    :param w: 指定范围, 参考找图函数
    :param h: 指定范围, 参考找图函数
    :param offset_x: 相对于找到的图片的位置横轴方向上的编译, 可以为负数, 取值范围为-1.0-1.0, 如找到图片的坐标x为100, 则点击坐标x=100 + offset_x * 屏幕宽
    :param offset_y: 相对于找到的图片的位置纵轴方向上的编译, 可以为负数, 取值范围为-1.0-1.0
    :param threshold: 引擎找图算法, 参考找图函数
    :param wait: 找到了图片等待多少秒再进行点击
    :return: 
    """
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
        log_d(f"█ 图片点击 █ {r[-1]} -> {x},{y}")
        return True
    else:
        return False


def ocr_exists_all(*text, x=None, y=None, w=None, h=None) -> bool:
    """
    使用ocr判断当前屏幕上是否所有文字都存在\n

    使用例子:若屏幕指定位置存在“去添加” 则找图进行点击
    ::
        ocr_exists_all("去添加", y=0.75, x=0.3, w=0.5) and find_image_click("img/今日头条开红包叉.jpg", y=0.5,
                                                                                        w=0.15, threshold=0)


    :param text: 可变参数, 要判断的文字
    :returns: 是否所有文字都存在
    """
    ocr_result = screen_ocr_x(text, x, y, w, h)
    return len(ocr_result) == len(text)


def ocr_exists_any(*text, x=None, y=None, w=None, h=None) -> bool:
    """
    使用ocr判断当前屏幕上是否任意文字存在\n

    使用例子:若屏幕指定位置存在任意文字 立即领取、拆、点击领取现金、立即提现、同意并继续, 则找图进行点击
    ::
        ocr_click_any("立即领取", "拆", "点击领取现金", "立即提现", "同意并继续", y=0.5, h=0.3) and toast("存在任意文字")

    :param text: 可变参数, 要判断的文字
    :returns: 是否任意文字都存在
    """
    ocr_result = screen_ocr_x(text, x, y, w, h)
    return len(ocr_result) > 0


def set_text(text):
    """
    设置编辑框的文本
    
    :param text: 需要设置到编辑框的文本
    :return: 无
    """
    x_input_clear()
    sleep(.5)
    x_input_clear()
    sleep(.5)
    x_input_text(text)


def open_app_from_desktop(app_name: str, pkg_name: str, img: str):
    """
    该函数模拟手动从手机桌面点开应用, 也可以使用open_app函数
    
    :param app_name: 应用名
    :param pkg_name: 应用包名
    :param img: 应用图标截图
    :returns 无
    """
    
    # 滑回到主页
    do(2, 1.5, False, key_home)
    # 翻动最多4页找到图标
    for _ in range(5):
        sleep(1)
        log_d(f"寻找[{app_name}]图标")
        t = screen_find_image_x((img,), min_prob=0.75, threshold=0)
        if t:
            log_d("找到图标, 进行点击")
            click_target(t[0])
            sleep(3)
            if device_foreground_package() == pkg_name:
                log_d("进入应用成功!")
                return True
        else:
            swipe_left()
    log_d(f"进入应用[{app_name}]失败!")
    return False


def exit_go_home():
    """
    返回桌面并退出当前脚本项目
    
    :return: 无
    """
    key_home()
    exit(0)


def find_image_click_max_prob(*img, min_prob=0.5, x=None, y=None, w=None, h=None, is_random_click=False,
                              threshold: int = -1) -> bool:
    """
    find_image_click的增强版本
    编写简单的游戏脚本非常实用, 思路传入一堆图片, 看看出现了哪些图片, 查找相似度最大的图片进行点击\n
    有些图片是必点的, 如应用提示的确认对话框
    
    :param img: 可变参数, 元素为图片字符串或者元祖(图片, 是否必须点击, 点击前停顿秒数, 点击次数)
    :param min_prob: 过滤置信率
    :param x: 指定范围, 参考找图函数
    :param y: 指定范围, 参考找图函数
    :param w: 指定范围, 参考找图函数
    :param h: 指定范围, 参考找图函数
    :param is_random_click: 是否随机点击
    :param threshold: 阈值
    :return: 是否找到了符合目标的图片并进行了点击操作
    """
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
        log_d("@1再次确认检测目标")
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
            log_d(f"█ 返回结果:" + str(img_res_single))
            if img_res_single.name in must_click:
                log_d(f"█ 发现必点图片: {img_res_single}")
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
        log_d(f"█ 最大可能性图片点击 █ {best_img} -> {best_img.cx},{best_img.cy}")
        return True
    else:
        return False
