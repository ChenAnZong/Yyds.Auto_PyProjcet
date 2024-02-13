import re
import colorsys


class Point:
    """
    坐标
    """

    def __init__(self, x: int, y: int):
        self.x = x  # 横轴
        self.y = y  # 纵轴

    def __str__(self):
        return f'Point({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()


class Color:
    """
    RGB颜色
    """

    def __init__(self, r: int, g: int, b: int):
        self.r = r  # 红色分量
        self.g = g  # 绿色分量
        self.b = b  # 蓝色分量

    def similarity_to(self, color2) -> float:
        """
        使用 HS 欧拉距离计算算法, 计算与另一个颜色的相似度

        :param color2: 另一个Color
        :returns: 0-1之间的浮点数, 数字越大, 两个颜色越相似
        """
        h1, s1, v1 = colorsys.rgb_to_hsv(self.r, self.g, self.b)
        h2, s2, v2 = colorsys.rgb_to_hsv(color2.r, color2.g, color2.b)

        hue_diff = min(abs(h1 - h2), 1 - abs(h1 - h2))
        saturation_diff = abs(s1 - s2)
        value_diff = abs(v1 - v2)
        similarity = (1 - hue_diff) * (1 - saturation_diff) * (1 - value_diff)

        return similarity

    def __str__(self):
        return f'Color({self.r},{self.g},{self.b})'

    def __repr__(self):
        return self.__str__()


class ResFindImage:
    """
    自动化引擎 封装高级查找图片(模版匹配算法)请求参数
    所有坐标均为屏幕绝对坐标
    """

    def __init__(self, name: str, path: str, prob: float, width: int, height: int, x: int, y: int):
        self.name = name  # 传入目标的图片路径参数
        self.path = path  # 传入目标的图片路径
        self.prob = prob  # 引擎计算的置信率
        self.width = width  # 匹配到的图片宽(浮点运算原因, 可能与传入图片的宽相差1像素)
        self.height = height  # 匹配到的图片高(浮点运算原因, 可能与传入图片的高相差1像素)
        self.x = x  # 左上角 x
        self.y = y  # 左上角 y

    @property
    def cx(self) -> int:
        return int(self.x + self.width / 2)

    @property
    def cy(self) -> int:
        return int(self.y + self.height / 2)

    def __str__(self):
        return f'ResFindImage {{ name=f"{self.name}", path=f"{self.path}", prob={self.prob}, width={self.width}, ' \
               f'height={self.height}, x={self.x}, y={self.y} }}'

    def __repr__(self):
        return str(self)


class ResYolo:
    """
    自动化引擎 封装高级查找图片(Yolo算法)返回结果
    所有坐标均为屏幕绝对坐标
    """

    def __init__(self, label: str, cx: int, cy: int, x: float, y: float, w: float, h: float, prob: float):
        self.label = label
        self.cx = cx  # 中间 x
        self.cy = cy  # 中间 y
        self.x = x  # 左上角 x
        self.y = y  # 左上角 y
        self.w = w  # 宽
        self.h = h  # 高
        self.prob = prob  # yolo 识别置信率, 范围0-1.0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'ResYolo {{label="{}", cx={}, cy={}, x={}, y={}, w={}, h={}, prob={} }}'.format(self.label, self.cx,
                                                                                               self.cy, self.x,
                                                                                               self.y, self.w, self.h,
                                                                                               self.prob)


class ResOcr:
    """
    自动化引擎 封装OCR识别返回结果
    所有坐标均为绝对坐标
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
        :returns: 中间坐标 x
        """
        return int((self.x1 + self.x3) / 2)

    @property
    def cy(self):
        """
        :returns: 中间坐标 y
        """
        return int((self.y1 + self.y3) / 2)

    @property
    def h(self):
        """
        :return: 高
        """
        return int(self.y3 - self.y2)

    @property
    def w(self):
        """
        :return: 宽
        """
        return int(self.x3 - self.x1)

    def __str__(self):
        return 'ResOcr# {{ prob={}, text="{}", x1={}, y1={}, x2={}, y2={}, x3={}, y3={}, x4={}, y4={} }}' \
            .format(self.prob, self.text, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4)

    def __repr__(self):
        return self.__str__()


class DeviceForegroundResponse:
    """
    设备前台运行的应用信息
    """
    def __init__(self, package: str, activity: str, pid: int):
        """
        :param package 进程包名
        :param activity 进程当前活动名
        :param pid 当前进程pid
        """
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
        return 'DeviceForegroundResponse {{ package="{}", activity="{}", pid={} }}'.format(self.package,
                                                                                           self.activity_name, self.pid)


class Node:
    """
    控件元素
    """

    def __init__(self, node_obj: dict):
        """
        初始化Node对象

        :param node_obj: 包含节点信息的字典对象
        :type node_obj: dict
        """
        self.bound_str: str = node_obj.get("boundsString")  # 控件的边界字符串描述
        self.child_count: int = node_obj.get("childCount")  # 子节点数量
        self.parent_count: int = node_obj.get("parentCount")  # 父节点数量
        self.class_name: str = node_obj.get("cls")  # 控件类名
        self.pkg: str = node_obj.get("pkg")  # 控件所在应用的包名
        self.text: str = node_obj.get("text")  # 控件文本内容
        self.desc: str = node_obj.get("desc")  # 控件描述
        self.id: str = node_obj.get("id")  # 控件ID
        self.hash_code = int(node_obj.get("hashCode"))  # 控件的唯一标识, 由引擎进行生成
        self.index: int = int(node_obj.get("index"))  # 控件索引
        self.is_check_able: bool = node_obj.get("isCheckable")  # 是否可被勾选
        self.is_clicked: bool = node_obj.get("isChecked")  # 是否被点击
        self.is_enable: bool = node_obj.get("isEnable")  # 是否可用
        self.is_foucuable: bool = node_obj.get("isFocusable")  # 是否可获取焦点
        self.is_foucesed: bool = node_obj.get("isFocused")  # 是否已获取焦点
        self.is_long_click_able: bool = node_obj.get("isLongClickable")  # 是否可长按
        self.is_password: bool = node_obj.get("isPassword")  # 是否为密码输入框
        self.is_scroll_able: bool = node_obj.get("isScrollable")  # 是否可以滚动
        self.is_selected: bool = node_obj.get("isSelected")  # 是否已被选中
        self.is_visible: bool = node_obj.get("isVisible")  # 是否可见
        self.dump_time_ms: int = node_obj.get("dumpTimeMs")  # 控件的显示时间, 非系统获取, 由引擎进行生成

    @property
    def cx(self) -> int:
        return self.center_point[0]

    @property
    def cy(self) -> int:
        return self.center_point[1]

    @property
    def center_point(self) -> (int, int):
        """
        返回节点的中间坐标点, 方便用于点击

        :returns: 中间坐标的x, y轴数值
        """
        s = [i for i in re.split(r"\[|\]|,", self.bound_str) if i != ""]
        x1 = int(s[0])
        y1 = int(s[1])
        x2 = int(s[2])
        y2 = int(s[3])
        return int((x1 + x2) / 2), int((y1 + y2) / 2)

    def __str__(self):
        return f"Node {{ class_name:{self.class_name}, bound_str:{self.bound_str}, child_count:{self.child_count}, " \
               f"parent_count:{self.parent_count}, pkg:{self.pkg}, text:{self.text}, desc:{self.desc}, id:{self.id}" \
               f"index: {self.index} click_able: {self.is_clicked} long_click_able: {self.is_long_click_able} " \
               f"is_scroll_able: {self.is_scroll_able} }}"

    def __repr__(self):
        return self.__str__()


class RequestFindImage:
    """
    引擎查找图片请求参数
    """

    def __init__(self, name: str, path: str, min_prob: float):
        self.name = name  # 传入的图片参数
        self.path = path  # 传入的图片路径
        self.min_prob = min_prob  # 要求最低置信率

    def __str__(self):
        return 'RequestFindImage {{ name="{}", path="{}", min_prob={} }}'.format(self.name, self.path, self.min_prob)

    def __repr__(self):
        return str(self)


class MatchImageResult:
    """
    引擎匹配图片返回结果
    """
    def __init__(self, x: int, y: int, w: int, h: int, prob: float):
        self.x = x  # 匹配到到左上角x坐标
        self.y = y  # 匹配到到左上角y坐标
        self.w = w  # 匹配图像的宽
        self.h = h  # 匹配图像的高
        self.prob = prob  # 匹配图像的相似度, 范围为0-1.0

    def __str__(self):
        return f"MatchImageResult(x={self.x}, y={self.y}, w={self.w}, h={self.h}, prob={self.prob})"

    def __repr__(self):
        return self.__str__()


class EngineResultParser:
    """
    引擎颜色字符串转化解析
    """

    @staticmethod
    def parse_color(rgb_text: str) -> Color:
        """
        从类似 255,255,125 这样的字符串解析获取实例
        """
        rgb_split = rgb_text.split(",")
        return Color(int(rgb_split[0]), int(rgb_split[1]), int(rgb_split[2]))

    @staticmethod
    def parse_multi_color(rgb_text: str) -> (Color,):
        """
        从以空格为分隔的多个颜色中解析获取实例数组
        """
        line_split = rgb_text.split(" ")
        ret = []
        for line in line_split:
            if len(line) > 4:
                rgb_split = line.split(",")
                ret.append(Color(int(rgb_split[0]), int(rgb_split[1]), int(rgb_split[2])))
        return tuple(ret)

    @staticmethod
    def parse_point(text: str) -> Point:
        """
        解析引擎的坐标字符串
        """
        point_split = text.split(",")
        return Point(int(point_split[0]), int(point_split[1]))

    @staticmethod
    def parse_match_result(text) -> MatchImageResult:
        """
        解析引擎的图片匹配结果
        """
        sp = re.split(",| ", text)
        return MatchImageResult(int(sp[1]), int(sp[2]), int(sp[3]), int(sp[4]), float(sp[0]))
