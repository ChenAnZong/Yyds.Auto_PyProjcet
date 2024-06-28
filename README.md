# 更加人性化的生产力安卓自动化脚本开发
![软件LOGO](https://yydsxx.com/img/snake.gif)

**- 🧞‍♂️本项目为 [Yyds.Auto](www.yydsxx.com) python api更新参考(可转化为其它语言的开发)以及作为脚本项目开发模版**

**- 安卓自动化开发、脚本开发、群控开发优质项目, 某种需求上替代[uiautomator2](https://github.com/openatx/uiautomator2)与替代[appium](https://github.com/appium/appium)**

# 特性
开箱即用, 无需注册, 可免APK安装运行, 可被易语言, auto.js等软件进行调用, 永久免费, 天然绿色产品, 居家必备, 包含大量人性化的安卓自动化功能的接口实现, 不依赖无障碍, 支持安卓7-14, 支持云机与模拟器, 同时支持电脑运行脚本与手机运行脚本

## 使用HTTP接口对自动化功能进行调用
如下192.168.1.100为手机设备IP地址, 61140为自动化引擎开放端口

### 点击
```shell
curl -X POST -d '{"x": 100, "y": 100}' http://192.168.1.100:61140/api/touch
```

```python
import requests
requests.post("http://192.168.1.100:61140/api/touch", json={
    "x": 100,
    "y": 100
})
```

### OCR
```shell
curl -X POST  http://192.168.1.100:61140/api/screen-ocr
```

```python
import requests
requests.post("http://192.168.1.100:61140/api/screen-ocr")
```



### 控件查找与匹配(支持正则匹配)
```shell
curl -X POST -d '{"text": "Add.*?"}' http://192.168.1.100:61140/api/ui-match
```

```python
import requests
requests.post("http://192.168.1.100:61140/api/ui-match", json={
    "text": "Add.*?"
})
```

### 🔥更多例子请参考源代码, 可根据自己项目修改定制群控

# 发现了错误或找到了bug
你真厉害, 可以提交issue与联系作者进行修改, 谢谢🙏

# 入门须知
1. 新手可以克隆或下载该项目作为模版, 进行脚本开发
2. 可同时运行在手机的Yyds.Auto上与电脑上(在电脑运行是通过http接口与引擎进行通讯, 在手机运行是反射调用自动化引擎函数)
3. 我们在开发项目的时候, 可以参考函数实现以及进行改动, 除了引擎接口通讯部分内容, 其它所有内容均可自行删减修改
4. 本工程包含一些用于学习以及测试的代码, 对于业务可能意义不大, 请自行分析并理解
5. 很多功能是可以自己去做的, 不一定要这个工程提供的, 比如我们要做压缩文件, 图片裁剪, 稍微百度一下就能做了嘞!


# 版本变更
[官方链接](https://yydsxx.com/docs/yyds-auto/update_history)

# 官方文档以及资源下载
[APK以及开发插件下载地址](https://yydsxx.com/download)

[文档网站 https://yydsxx.com/docs/yyds-auto/script](https://yydsxx.com/docs/yyds-auto/script)

# 文件指引
| 文件/目录             | 重要性 | 作用                            |
|----------------------|-----|-------------------------------|
| main.py              | 必须  | 程序**入口**文件                    |  
| project.config       | 必须  | 项目**配置**文件                    |
| yyds/auto_func.py    | 可删  | 实用自动化项目装饰器函数                  |
| yyds/auto_api.py     | 必须  | 基本的自动化功能实现                    |
| yyds/auto_api_aux.py | 重要  | 次要的自动化功能实现                    |
| yyds/auto_plus.py    | 可删  | 拓展的自动化功能实现                    |
| yyds/auto_entity.py  | 可删  | 自动化相关实体类, 如坐标, 颜色等            |
| yyds/util.py         | 可删  | 实用自动化工具函数, 如日志                |
| ui.yml               | 可删  | 项目界面配置文件, 如果不需要任何`界面配置`, 则可删除 |  
| _img_                | 重要  | 区域截图默认保存位置, 一般找图的图片保存在此目录下    |  
| content.txt          | 可删  | 测试文本读取的文件                     |
| README.md            | 可删  | 项目介绍文件                        |  

# 其它
## Yyds.Auto 开发插件源代码
[开发插件 https://github.com/ChenAnZong/Yyds.Auto-IntellIjDevPlugin.git](https://github.com/ChenAnZong/Yyds.Auto-IntellIjDevPlugin.git)

## 视频教程
[Yyds.Auto Python自动化脚本开发(Bilibli!)](https://space.bilibili.com/413090517)

## 支持使用Shizuku激活
[Shizuku官网 https://shizuku.rikka.app/](https://shizuku.rikka.app/)

# 联系交流
[联系作者 | QQ交流群](https://yydsxx.com/contact)