from .auto_api import *


def click_double(x: Union[str, int], y: Union[str, int]):
    """
    双击坐标点
    """
    click(x, y)
    time.sleep(290)
    click(x, y)


def swipe(x1, y1, x2, y2, duration, is_random: bool = False):
    """
    滑动

    :param x1: 起始坐标 x
    :param y1: 起始坐标 y
    :param x2: 目标坐标 x
    :param y2: 目标坐标 y
    :param duration: 滑动耗时（毫秒） 越小滑动越快
    :param is_random: 是否随机进行滑动(会画出一条锯齿一样的线, 而不是纯直线)
    """
    engine_api("/swipe", {"x1": int(x1), "x2": int(x2),
                          "y1": int(y1), "y2": int(y2), "duration": int(duration), "random": is_random})


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
    注入键值码, 键值码数值, 请参考yydsxx.com, 参考文章[Android KeyCode 键码对照表](http://yydsxx.com/blog/android%20keycode%20table)

    :param code: 键值码
    """
    engine_api("/key-code", {"code", int(code)})


def device_get_screen_size() -> (int, int):
    """
    获取屏幕分辨率大小

    ⚠️ 注意:竖屏与横屏返回的数值在屏幕发生旋转时候不一样, 比如竖屏时候, 返回(1080, 1920); 在横屏时候, 返回(1920, 1080), 我们在使用百分比坐标系统时候尤其需要注意这一点
    :returns: 宽, 高
    """
    ret = engine_api("/screen-size")
    x, y = ret.split(",")
    return int(x), int(y)


def stop_app(pkg):
    """
    停止应用运行, 相当于从任务栏划掉app

    :returns: 无
    """
    return shell(f"am force-stop {pkg}")


def open_app(pkg):
    """
    根据包名打开应用

    :params: 应用包名, 如系统不便查看应用包名, 可通过如"设备信息"等三方应用进行查看
    :returns: 无
    """
    return engine_api("/open-app", {"pkg": pkg})


def open_url(url):
    """
    通过匹配intent打开网页, 电话等页面, 会使用系统默认应用进行打开\n
    如果 url为 http 链接, 即使用系统默认的浏览器应用, 也能打开其它系统链接 比如电话tel:21113336\n
    成功返回:Starting: Intent { act=android.intent.action.VIEW dat=tel:xxxxxxxxxx }\n
    错误返回:Starting: Intent { act=android.intent.action.VIEW dat=asdfs } Error: Activity not started, unable to resolve Intent { act=android.intent.action.VIEW dat=asdfs flg=0x10000000 }

    :returns: intent 命令的输出
    """
    return engine_api("/open-url", {"url": url})


def device_foreground() -> Optional[DeviceForegroundResponse]:
    """
    获取当前设备前台运行信息

    :returns: 前台运行信息, 包含有当前进程pid, 活动名, 应用包名信息
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

    :param pkg: 应用包名
    :returns: 当前当前是否在某应用界面内
    """
    return pkg == device_foreground_package()


def device_code() -> str:
    """
    应用imei码, 可作为应用唯一硬件码, 如获取失败则获取meid或者cpu序列号

    :returns: 唯一设备硬件码
    """
    return engine_api("/imei")


def device_model() -> str:
    """
    获取当前手机型号
    学习指南:类似命令可以自定义很多, 比如获取当前设备代号 ``shell("getprop ro.product.device")``

    :returns: 手机型号
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

    :param ncnn_bin_path: bin文件路径
    :param ncnn_param_path: param文件路径
    :returns: 无
    """
    engine_api("/set-yolo-model", {
        "bin_file_path": ncnn_bin_path,
        "param_file_path": ncnn_param_path
    })


def model_ocr_reload(ncnn_bin_path, ncnn_param_path):
    """
    自定义你的pp ocr模型, 需要转换为ncnn模型, 若已经加载过模型, 则进行重新加载\n
    提示: 引擎已内置OCR模型, 一般不用自己训练, 如需要艺术字识别等场景可以自行训练

    :param ncnn_bin_path: bin文件路径
    :param ncnn_param_path: param文件路径
    :returns: 无
    """
    engine_api("/set-ocr-model", {
        "bin_file_path": ncnn_bin_path,
        "param_file_path": ncnn_param_path
    })


def ui_match(all_window=False, match_from_cache=False, **match_params) -> List[Node]:
    """
    扫描当前屏幕所有ui控件并进行匹配\n

    ::

        # 注意因为python中变量命名无法包含横杠-, 所以使用_代替, class用class_代替
        ui_match(context_desc="资讯", drawing_order="2")


    **支持以下匹配规则**\n
    1. 使用正则(适用java正则)
    2. 使用范围限定(可使用大于小于号进行数值限定)
    3. 结合父子兄关系进行定位
        - 所有父节点 以par_开头
        - 所有兄节点 以sib_开头
        - 所有子节点 以chi_开头
    4. 使用控件尺寸进行定位, 支持 > 与 < 符号进行范围指定
        - width 宽
        - height 高
    5. 限制控件屏幕方位
        - top 上
        - bottom 下
        - left 左
        - right  右
    \n
    匹配例子:

    ::

        # 结合位置, 大于进行定位, top=0.5意思是从屏幕中间往下开始找, width>10 意思是控件的宽大于10
        ui_match(text="我的", top=0.5, width=">10")

    :param all_window: 是否查找所有窗口(一般app不用, 为了查找悬浮窗, 特殊系统控件用), 如果从缓存中查找, 此参数将被忽略
    :param match_params: 匹配参数, 有多个匹配参数就需要匹配全部参数
    :param match_from_cache: 是否从引擎缓存中拉取控件, 而不是从系统从新获取控件; 适合于确保当前画面没有变化的界面, 提高运行效率
    :returns: 识别结果, 匹配到的节点数组, 如匹配失败, 返回空数组
    """
    params_ = {"match_from_cache": "true" if match_from_cache else "false"}
    for k in match_params.keys():
        if k == "class_":
            params_["class"] = match_params[k]
        else:
            params_[str(k).replace("_", "-")] = match_params[k]
    if not match_from_cache and all_window:
        params_["all_window"] = "true"
    ret_str = engine_api("/uia-match", params_)
    return [Node(i) for i in json.loads(ret_str)]


def ui_parent(node: Node) -> List[Node]:
    """
    获取一个节点的父节点
    注意父节点是往上遍历的, 即结果数组后面的元素是前面元素的父节点

    :returns: 匹配到的节点数组, 如匹配失败, 返回空数组
    """
    params_ = {
        "hashcode": node.hash_code,
        "dump_time_ms": node.dump_time_ms,
        "type": "parent"
    }
    ret_str = engine_api("/uia-relation", params_)
    return [Node(i) for i in json.loads(ret_str)]


def ui_child(node: Node) -> List[Node]:
    """
    获取一个节点的子节点

    :returns: 匹配到的节点数组, 如匹配失败, 返回空数组
    """
    params_ = {
        "hashcode": node.hash_code,
        "dump_time_ms": node.dump_time_ms,
        "type": "child"
    }
    ret_str = engine_api("/uia-relation", params_)
    return [Node(i) for i in json.loads(ret_str)]


def ui_sib(node: Node) -> List[Node]:
    """
    获取一个节点的旁系节点(兄弟节点), 结果不包含自己

    :returns: 匹配到的节点数组, 如匹配失败, 返回空数组
    """
    params_ = {
        "hashcode": node.hash_code,
        "dump_time_ms": node.dump_time_ms,
        "type": "sib"
    }
    ret_str = engine_api("/uia-relation", params_)
    return [Node(i) for i in json.loads(ret_str)]


def ui_exist(all_window=False, match_from_cache=False, **match_params) -> bool:
    """
    检查符合条件的控件是否存在
    :param all_window: 是否查找所有窗口
    :param match_from_cache: 是否从引擎缓存中拉取控件, 而不是从系统从新获取控件; 适合于确保当前画面没有变化的界面, 提高运行效率
    :returns: ui是否存在
    """
    params_ = {"match_from_cache": "true" if match_from_cache else "false"}
    match_params["limit"] = 1
    for k in match_params.keys():
        if k == "class_":
            params_["class"] = match_params[k]
        else:
            params_[str(k).replace("_", "-")] = match_params[k]
    if not match_from_cache and all_window:
        params_["all_window"] = "true"
    return len(engine_api("/uia-match", params_)) > 1


def shell(*cmd):
    """
    自动化引擎 执行shell脚本, 返回shell字符串, 可执行多条
    注意引擎内置busybox, PATH的优先级在最前面的是:/data/local/tmp/BB
    :returns: 返回shell执行输出 包括错误流!
    """
    return engine_api("/shell", {"cmd": ";".join(cmd)})


def screen_find_image_x(fd_images: Union[Tuple[str, ...], Tuple[RequestFindImage, ...]],
                        min_prob: float = 0.5, x=None, y=None, w=None, h=None, threshold: int = -1) \
        -> Tuple[ResFindImage]:
    """
    对于同时查找多张图片的封装

    :param fd_images: 需要查找的图片, 图片数组或元祖, 需要一个可迭代的对象
    :param min_prob:  float 最低置信率
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param threshold: 图片预处理方式 参考`screen_find_image()`
    :rtype: Tuple[ResFindImage]
    :returns: 找图结果
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
    屏幕查找图片, 仅返回第一张查找结果

    :param fd_images: 需要查找的图片
    :param min_prob:  最低置信率
    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param threshold: 图片预处理方式 参考`screen_find_image()`
    :return: 第一张查找到到图片
    """
    find_images = screen_find_image_x(*fd_images, min_prob=min_prob, x=x, y=y, w=w, h=h, threshold=threshold)
    if len(find_images) > 0:
        return find_images[0]
    return None


def screen_yolo_find_x(specify_labels=None, min_prob: float = 0.9, x=None, y=None, w=None, h=None, use_gpu=False) \
        -> Tuple[ResYolo]:
    """
    通过yolo算法识别当前屏幕内容, 注意使用model_yolo_reload函数正确加载自定义模型, 否则加载默认的目录下模型

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
    :returns: 请参考yolo_find_x, 返回第一个结果
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
    使用内置ocr模型 对当前屏幕进行 OCR 识别

    :param x: 识别起始点 可以使用相对坐标(0-1)
    :param y: 识别起始点 可以使用相对坐标(0-1)
    :param w: 宽 可以使用相对坐标(0-1)
    :param h: 高 可以使用相对坐标(0-1)
    :param use_gpu: 是否使用Gpu运算, 性能差的手机不建议, 会导致手机掉帧
    :param specific_texts: 指定查找文本, 支持 python正则表达式匹配
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
    使用内置ocr模型 对当前屏幕进行 OCR 识别, 但只获取第一个返回结果

    :returns: 可参考screen_ocr_x , 返回第一个结果
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
    计算两张的图片相似度, 注意需要两张图片的尺寸一致

    :param img1: 图片1的路径
    :param img2: 图片2的路径
    :param flags: 若为0则使用直方图计算; 未来会增加更多的对比算法
    :returns: 返回0-100的浮点数
    """
    return float(engine_api("/image-similarity", {"image1": img1, "image2": img2, "flags": flags}))


def input_text(text: str) -> int:
    """
    注入文本, 受安卓系统限制, 不支持中文

    :param text: 文本, (ascii)进允许包含英文数字以及符号
    :returns: 注入成功的字符个数
    """
    return int(engine_api("/inject-text", {"text": str(text)}))


def x_input_text(text: str) -> bool:
    """
    通过内置 YY 自动输入法输入文本, 需要手动到系统设置启动输入法并切换输入法(或在root下从Yyds.Auto菜单中一键启动)\n
    [更多关于YY输入法的资料](/docs/yyds-auto/yy-input)

    :returns: 仅代表是否发送成功到引擎, 不代表是否执行成功
    """
    return engine_api("/xinput-text", {"text": str(text)}) == "true"


def x_input_clear() -> bool:
    """
    通过内置 YY 自动输入法清空编辑框文本, 需要手动到系统设置启动输入法并切换输入法(或在root下从Yyds.Auto菜单中一键启动)\n
    [更多关于YY输入法的资料](/docs/yyds-auto/yy-input)

    :returns: 仅代表是否发送成功到引擎, 不代表是否执行成功
    """
    return engine_api("/xinput-clear") == "true"


def set_yy_input_enable(enable: bool) -> bool:
    """
    启用或禁用YY输入\n
    [更多关于YY输入法的资料](/docs/yyds-auto/yy-input)

    :param enable: 设置为False 若当前为YY输入法, 退出并切换回上个输入法
    :returns: 是否已启用
    """
    return engine_api("/enable-yy-input", {"enable": "true" if enable else "false"}) == "true"


def app_data_backup(pkg: str, path: str) -> bool:
    """
    备份应用数据到指定的路径

    :param pkg: 应用包名
    :param path: 备份路径, 备份文件为tar格式
    :returns: 是否成功
    """
    return engine_api("/backup-app-data", {"package": pkg, "path": path}) == "true"


def app_data_recovery(pkg: str, path: str) -> bool:
    """
    从指定的文件还原应用数据

    :param pkg: 应用包名
    :param path: 备份路径, 备份文件为tar格式, 如/sdcard/1.tar.gz
    :returns: 是否成功
    """
    return engine_api("/recovery-app-data", {"package": pkg, "path": path}) == "true"


def app_apk_backup(pkg: str, path: str) -> bool:
    """
    提取备份应用安装包(apk), 保存到设备指定位置

    :param pkg: 应用包名
    :param path: 备份到手机路径
    :returns: 是否成功
    """
    apk_path = shell(f"pm path {pkg}").replace("package:", "")
    if "data" in apk_path:
        shell(f"cat {apk_path} > {path}")
        return True
    else:
        return False


def app_apk_install(path: str) -> bool:
    """
    进行 apk 安装

    :param path: APK文件路径
    :returns: 是否安装成功
    """

    # 如果apk文件在外置存储目录, 我们需要移动到其它可以安装到位置, 否则会报错!
    if "/sdcard/" in path or "/storage/emulated/0/" in path:
        return "success" in shell(
            f"mv {path} /data/local/tmp/temp.apk && pm install -r /data/local/tmp/temp/apk && echo success")
    return "success" in shell(f"pm install -r {path} && echo success")


def set_clipboard(text: str):
    """
    复制文本到粘贴板, 在高级的安卓版本可能被受到限制, 注意自行测试, 在高版本安卓中, 应启用YY输入法方可进行稳定的获取

    :param text: 要复制粘贴到文本
    :returns: 无
    """
    engine_api("/paste", {text: text})


def get_clipboard() -> str:
    """
    获取粘贴板文本, 在安卓9以上被限制, 需要启用YY输入法进行获取

    :returns: 粘贴板文本
    """
    return engine_api("/clipboard-text", {})
