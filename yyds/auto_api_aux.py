from .auto_api import *


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


def key_menu():
    """
    注入菜单键
    """
    engine_api("/key-code", {"code": "82"})


def key_confirm():
    """
    确认键，一般用于编辑框确实搜索，确认提交
    """
    return engine_api("/key-confirm")


def key_code(code):
    """
    注入键值码, 键值码数值, 请参考yydsxx.com <<Android KeyCode 键码对照表>>
    @param code 键值码
    """
    engine_api("/key-code", {"code", int(code)})


def device_get_screen_size() -> (int, int):
    """
    获取屏幕分辨率大小
    ⚠️ 注意:竖屏与横屏返回的数值在屏幕发生旋转时候不一样, 比如竖屏时候, 返回(1080, 1920); 在横屏时候, 返回(1920, 1080), 我们在使用百分比坐标系统时候尤其需要注意这一点
    :returns 宽, 高
    """
    ret = engine_api("/screen-size")
    x, y = ret.split(",")
    return int(x), int(y)


def stop_app(pkg):
    """
    停止应用运行, 相当于从任务栏划掉app
    """
    return shell(f"am force-stop {pkg}")


def open_app(pkg):
    """
    根据包名打开app
    """
    return engine_api("/open-app", {"pkg": pkg})


def open_url(url):
    """
    打开系统u rl
    如果 url为 http 链接, 即使用系统默认的浏览器应用
    也能打开其它系统链接 比如电话tel:21113336
    成功返回:Starting: Intent { act=android.intent.action.VIEW dat=tel:xxxxxxxxxx }
    错误返回:Starting: Intent { act=android.intent.action.VIEW dat=asdfs } Error: Activity not started, unable to resolve Intent { act=android.intent.action.VIEW dat=asdfs flg=0x10000000 }
    """
    return engine_api("/open-url", {"url", url})


def device_foreground() -> Optional[DeviceForegroundResponse]:
    """
    当前设备信息
    :returns: 当前包名, 当前应用Activity名(有时相对, 有时绝对取决于应用), 应用进程 pid
    """
    result = engine_api('/foreground')
    s = result.split(" ")
    if len(s) < 2:
        return None
    return DeviceForegroundResponse(s[0], s[1], s[2])


def device_foreground_activity() -> str:
    """
    比device_foreground 更快 
    :returns: 当前活动界面名
    """
    return engine_api("/foreground-fast")


def device_foreground_package() -> str:
    """
    比device_foreground 更快 
    :returns: 当前前台包名
    """
    return engine_api("/foreground-pkg")


def is_app_running(pkg: str) -> bool:
    """
    :returns: app是否在后台运行
    """
    return engine_api("/background-is-running", {"pkg": pkg}) == "true"


def bring_app_to_top(pkg: str) -> bool:
    """
    将后台运行的应用带回前台
    :returns: 是否操作成功
    """
    return engine_api("/background-to-top", {"pkg": pkg}) == "true"


def is_in_app(pkg: str) -> bool:
    """
    当前是否在某应用界面内
    :param pkg 应用包名
    """
    return pkg == device_foreground_package()


def device_code():
    """
    应用imei码, 可作为应用唯一硬件码, 提醒:在root下此码可被轻易篡改返回结果
    :returns: str
    """
    return engine_api("/imei")


def device_model() -> str:
    """
    当前手机型号, 类似命令可以自定义很多, 比如获取当前设备代号 ```shell("getprop ro.product.device")```
    """
    return shell("getprop ro.product.model")


def is_net_online() -> bool:
    """
    通过请求指定链接测试当前网络是否畅通
    :returns: 当前设备网络是否连通
    """
    return engine_api("/is-net-online") == "true"


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


def ui_match(match_from_cache=False, **match_params) -> List[Node]:
    """
    当前屏幕ui控件定位
    :param match_from_cache 是否从最后一次dump的缓存中匹配 可以加快搜索速度
    :returns: 识别结果
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


def shell(*cmd):
    """
    自动化引擎 执行shell脚本, 返回shell字符串, 可执行多条
    :returns: 返回shell执行输出 包括错误流!
    """
    return engine_api("/shell", {"cmd": ";".join(cmd)})


def screen_find_image_x(fd_images: Union[Tuple[str, ...], Tuple[RequestFindImage, ...]],
                        min_prob: float = 0.5, x=None, y=None, w=None, h=None, threshold: int = -1) \
        -> Tuple[ResFindImage]:
    """
    查看图片
    :param fd_images 需要查找的图片
    :param min_prob  float 最低置信率
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param threshold 图片预处理方式 参考`screen_find_image()`
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
    str_fds: str = screen_find_image(*fd_paths, x=x, y=y, w=w, h=h, threshold=threshold)
    sp_fds = str_fds.split('\n')
    results: List[ResFindImage] = list()
    index = 0
    for fd in sp_fds:
        try:
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
                if fd_image.prob >= it.min_prob:
                    results.append(fd_image)
                index = index + 1
        except:
            continue
    return tuple(results)


def screen_find_image_first_x(fd_images: Tuple[Union[str, RequestFindImage]], min_prob: float = 0.9,
                              x=None, y=None, w=None, h=None, threshold: int = -1) -> Union[ResFindImage, None]:
    """
    # 屏幕查找图片, 仅返回第一张查找结果

    :param fd_images 需要查找的图片
    :param min_prob  最低置信率
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param threshold 图片预处理方式 参考`screen_find_image()`
    :return: 第一张查找到到图片
    """
    find_images = screen_find_image_x(*fd_images, min_prob=min_prob, x=x, y=y, w=w, h=h, threshold=threshold)
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
    :param specific_texts 指定查找文本, 支持 python正则表达式匹配
    :returns: OCR识别结果列表
    """
    if isinstance(specific_texts, str):
        specific_texts = (specific_texts,)
    if specific_texts is None:
        specific_texts = []
    fd_ocr_str: str = ocr(x=x, y=y, w=w, h=h, use_gpu=use_gpu)
    fd_sp = fd_ocr_str.split('\n')
    results: List[ResOcr] = list()
    for find_text in specific_texts:
        for fd in fd_sp:
            if fd != "":
                prob, text, pos_split = fd.split('\t')
                result = re.match(r'(\d+),(\d+) (\d+),(\d+) (\d+),(\d+) (\d+),(\d+)', pos_split).groups()
                res = ResOcr(prob, text, int(result[0]), int(result[1]), int(result[2]), int(result[3]),
                             int(result[4]), int(result[5]), int(result[6]), int(result[7]))
                if re.match(find_text, res.text):
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


def image_similarity(img1: str, img2: str, flags: int = 0) -> float:
    """
    计算两张的图片相似度, 需要两张图片的尺寸一致
    :param img1 图片1的路径
    :param img2 图片2的路径
    :param flags = 0 使用直方图计算; 未来会增加更多的对比算法
    :returns: 返回0-100的浮点数
    """
    return float(engine_api("/image-similarity", {"image1": img1, "image2": img2, "flags": flags}))


def input_text(text: str) -> int:
    """
    注入文本, 受安卓系统限制, 不支持中文
    """
    return int(engine_api("/inject-text", {"text": str(text)}))


def x_input_text(text: str) -> bool:
    """
    通过内置 YY 自动输入法输入文本, 需要手动到系统设置启动输入法并切换输入法(或在root下从Yyds.Auto菜单中一键启动)
    :returns: 仅代表是否发送成功到, 不代表是否执行成功
    """
    return engine_api("/xinput-text", {"text": str(text)}) == "true"


def x_input_clear() -> bool:
    """
    通过内置 YY 自动输入法清空编辑框文本, 需要手动到系统设置启动输入法并切换输入法(或在root下从Yyds.Auto菜单中一键启动)
    :returns: 仅代表是否发送成功, 不代表是否执行成功
    """
    return engine_api("/xinput-clear") == "true"


def set_yy_input_enable(enable: bool) -> bool:
    """
    启用或禁用YY输入法
    """
    return engine_api("/enable-yy-input", {"enable": "true" if enable else "false"}) == "true"


def app_data_backup(pkg: str, path: str) -> bool:
    """
    :param pkg 应用包名
    :param path 备份路径, 备份文件为tar格式
    备份应用数据
    """
    return engine_api("/backup-app-data", {"package": pkg, "path": path}) == "true"


def app_data_recovery(pkg: str, path: str) -> bool:
    """
    :param pkg 应用包名
    :param path 备份路径, 备份文件为tar格式, 如/sdcard/1.tar.gz
    还原应用数据
    """
    return engine_api("/recovery-app-data", {"package": pkg, "path": path}) == "true"


def app_apk_backup(pkg: str, path: str) -> bool:
    """
    提取备份应用安装包(apk), 保存到设备指定位置
    :param pkg 应用包名
    :param path 备份到手机路径
    """
    apk_path = shell(f"pm path {pkg}").replace("package:", "")
    if "data" in apk_path:
        shell(f"cat {apk_path} > {path}")
        return True
    else:
        return False


def app_apk_install(path: str) -> bool:
    """
    apk 安装
    :param path 文件路径
    :returns 是否安装成功
    """
    # 如果apk文件在外置存储目录, 我们需要移动到其它可以安装到位置, 否则会报错!
    if "/sdcard/" in path or "/storage/emulated/0/" in path:
        return "success" in shell(
            f"mv {path} /data/local/tmp/temp.apk && pm install -r /data/local/tmp/temp/apk && echo success")
    return "success" in shell(f"pm install -r {path} && echo success")


def paste(text: str):
    """
    :param text 要复制粘贴到文本
    复制文本到粘贴板, 在高级的安卓版本可能被受到限制, 注意自行测试
    """
    engine_api("/paste", {text: text})


def get_clipboard():
    """
    获取粘贴板文本, 在安卓9以上被限制, 需要启用YY输入法进行获取
    """
    return engine_api("/clipboard-text", {})
