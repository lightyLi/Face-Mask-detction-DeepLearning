# 双创项目总结
- [双创项目总结](#双创项目总结)
    - [项目介绍](#项目介绍)
    - [系统框图](#系统框图)
      - [1. 系统框图](#1-系统框图)
    - [数据集及标注](#数据集及标注)
      - [1. 数据集获取](#1-数据集获取)
      - [2. 标注](#2-标注)
      - [3. 标注好的数据集](#3-标注好的数据集)
    - [训练过程及模型转换](#训练过程及模型转换)
    - [硬件模块介绍](#硬件模块介绍)
      - [1. 数据采集单元](#1-数据采集单元)
        - [1）摄像头模块](#1摄像头模块)
        - [2）红外测温模块](#2红外测温模块)
      - [2. 中央处理单元](#2-中央处理单元)
      - [3. 输出单元](#3-输出单元)
        - [1）LCD显示单元](#1lcd显示单元)
        - [2）音频模块](#2音频模块)
        - [3）舵机模块](#3舵机模块)
    - [总体控制代码](#总体控制代码)
    - [创新之处和遇到问题的解决](#创新之处和遇到问题的解决)
      - [1. 研发过程中遇到的问题](#1-研发过程中遇到的问题)
        - [1）测温模块在程序运行中一直返回温度值，是测得的环境温度](#1测温模块在程序运行中一直返回温度值是测得的环境温度)
        - [2） 口罩识别模型会对摄像头采集的每一帧图像进行识别，如果对模型输出的每一个预测结果做出反应的话，会造成系统过于混乱](#2-口罩识别模型会对摄像头采集的每一帧图像进行识别如果对模型输出的每一个预测结果做出反应的话会造成系统过于混乱)
        - [3） 由于K210开发板可用接口有限，在正常的插上测温模块后就不能插舵机模块了。](#3-由于k210开发板可用接口有限在正常的插上测温模块后就不能插舵机模块了)
      - [2. 测试阶段遇到的问题](#2-测试阶段遇到的问题)
        - [1） 语音播报模块在播放完音频后会有一声比较短暂刺耳的爆音](#1-语音播报模块在播放完音频后会有一声比较短暂刺耳的爆音)
        - [2） 模型对测试数据集预测效果不好，准确率较低](#2-模型对测试数据集预测效果不好准确率较低)
    - [不足待改进之处](#不足待改进之处)
      - [1. 弱光条件下识别准备率有待提升](#1-弱光条件下识别准备率有待提升)
        - [1） 原因](#1-原因)
        - [2） 建议改进措施](#2-建议改进措施)
      - [2. 远距离识别准确率不高](#2-远距离识别准确率不高)
        - [1） 原因](#1-原因-1)
        - [2） 建议改进措施](#2-建议改进措施-1)
      - [3. 测温模块精度不高](#3-测温模块精度不高)
        - [1） 原因](#1-原因-2)
        - [2） 建议改进措施](#2-建议改进措施-2)
    - [产品图](#产品图)
      - [1. 内部结构](#1-内部结构)
      - [2. 产品外观图](#2-产品外观图)
    - [参考资料](#参考资料)
    - [开源声明](#开源声明)
### 项目介绍

​	人脸口罩佩戴识别监测系统是一款集口罩识别、体温检测、语音播报和门闸开合于一体的智能识别反馈系统，它利用yolov2神经网络训练生成的模型进行人脸识别，具有较高的准确性、较低的时延等特性。

​        该设备能够针对口罩佩戴情况进行不同的内容反馈，并且语音提示，如果符合通过条件，可以控制闸机进行人员分流，非常适合当前后疫情时代的公共场所的疫情防控需求。

### 系统框图

#### 1. 系统框图

![image-20220523201259114](C:\Users\13213\AppData\Roaming\Typora\typora-user-images\image-20220523201259114.png)

![img](file:///C:/Users/13213/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png)

**注：** 系统框图与最终实现有所差别

### 数据集及标注

#### 1. 数据集获取

训练的数据集是来自互联网的公开数据集，链接如下：

https://github.com/cabani/MaskedFace-Net，里面有正确佩戴口罩和不正确佩戴口罩的数据集，各有20Gb左右。

https://github.com/balajisrinivas/Face-Mask-Detection/tree/master/dataset，里面有未佩戴口罩的数据集

我们用到的K210开发板在运行图像识别的时候，模型只能输入224*224大小的图片，所以需要先将数据集大小调整为**224\*224**.

#### 2. 标注

用到的标注软件为 **labelImg**,下载链接为：https://wwt.lanzoul.com/iAXAG05bnjxc，

或其他标注软件也可以，需要把标注结果导出为xml格式

#### 3. 标注好的数据集

下载链接如下，

pics:      https://www.aliyundrive.com/s/cRFP1YaU9WM

labels:   https://www.aliyundrive.com/s/uMY9xoWPovu

pics文件夹里存放图片，分为三类：with_correct_mask/with_incorrect_mask/without_mask

labels文件夹中存放标签，为xml格式

**注：** 用开发板的摄像头拍摄多张照片多为数据集的一部分可以提高模型的识别精度

### 训练过程及模型转换

由于K210开发板只支持YOLOV2和V3，我们采用YOLOV2框架来进行训练

环境配置及训练方法见链接：

[Mx-yolov3+Maixpy+ K210进行本地模型训练和目标检测_我与nano的博客-CSDN博客_k210芯片](https://blog.csdn.net/qq_51963216/article/details/121044449?utm_source=app&app_version=5.1.1)

[[人工智能\]更新：Mx-yolov3 3.0版本 (qq.com)](https://mp.weixin.qq.com/s/OpFfBedx2MrLX7QeQBJPrw) 

K210开发板只能运行kmodel格式的模型文件，所以需要将训练好的tilite、pt、h5等格式的模型转换成kmodel格式的模型。我们采用的是**NCC**工具箱，上面的链接中有提到。

### 硬件模块介绍

#### 1. 数据采集单元

##### 1）摄像头模块

+ OV5640摄像头模块是一颗1/4寸的CMOS UXGA（1632*1232）图像传感器，为标准24P接入，主要用于pyAI-K210配套开发，可以通过FPC排线延长获得更好的扩展性。具有五百万像素，供电电压为3.3V，输出格式为RGB565/555，8位压缩数据。标准镜头下的图片会出现一定的畸变（图像变形)，但并不影响图像识别，可以通过使用无畸变镜头解决这个问题。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.1.1 摄像头模块（pyAI-K210 CAM）.png" alt="图4.1.1 摄像头模块（pyAI-K210 CAM）" style="zoom:80%;" />

+ **摄像头接口方式**：pyAI-K210开发板通过FPC排线与摄像头模块连接。排线接线方式均为下接（排线金手指朝下）。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.1.2摄像头连接方式（金手指朝下） .png" alt="图4.1.2摄像头连接方式（金手指朝下） " style="zoom:80%;" />

+ **实现方式**：摄像头模块通过软件代码的实现首先需要确保硬件即摄像头模块已经正确的连接在pyAI-K210开发板上且开发板中有正确的驱动程序和对应的python程序文件。然后导入sensor模块即摄像头OV2640模块并初始化，然后OV2640模块将获得实时图像数据，并将图像数据通过FPC排线传输到pyAI-K210开发板中并开始被处理。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.1.3 摄像头模块流程图.png" alt="图4.1.3 摄像头模块流程图" style="zoom:80%;" />

| 模块方案 | OV5640                   |
| -------- | ------------------------ |
| 控制方式 | SCCB                     |
| 接口定义 | 24P-0.5mm FPC座          |
| 像素     | 最高1600*1200  （200万） |
| 模块尺寸 | 38*21mm                  |
| 适用平台 | pyAI-K210                |

##### 2）红外测温模块

+ MLX90614是一款无接触式的红外线温度感应芯片。它在同一TO-39封装内整合了红外热电堆感应器与一款定制的信号调节芯片。MLX90614在信号调节芯片中使用了先进的低噪音放大器，一枚17-bit ADC以及功能强大的DSP元件, 从而实现高精度温度测量。MLX90614 应用了 SMBus 和 PWM 两种数字输出方式.。出厂设定为 SMBus. 在无特殊设定情况下, 10 – bit PWM 输出可测量 -20-120 ̊C 温度范围，解析度为0.14 ̊C。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.2.1 测温模块(MLX90614).png" alt="图4.2.1 测温模块(MLX90614)" style="zoom:80%;" />

+ **连接方式**：pyAI-K210 是通过I2C总线与测温模块通讯的。具体的接口对应关系为：IO27→Y6→SCL，IO28→Y8→SDA。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.2.2 测温模块连接方式.png" alt="图4.2.2 测温模块连接方式" style="zoom:60%;" />

+ **实现方式**：该测温模块主要由软件代码实现，首先需要导入I2C、OLED、MXL90614模块，其次初始化I2C、OLED和MXL90614，此时MXL90614观测的数据将在I2C上进行显示。软件实现之后先将硬件连接到Py-base的I2C口，需要将SSD1306K.py这个驱动文件拷贝到pyAI-K210板子的文件系统中，通过发送文件到开发板，便可进行工作。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.2.3  测温模块流程图.png" alt="图4.2.3  测温模块流程图" style="zoom:80%;" />

| 控制接口     | I2C从机或PWM               |
| ------------ | -------------------------- |
| 测量距离     | DCC（10cm）和DCI（100cm）  |
| 测量范围     | -70℃至382.2℃               |
| 测量误差     | ±0.5℃（室温下）分辨率0.02℃ |
| 工作电压     | 3.3V至5V                   |
| 使用环境温度 | -40℃至125℃                 |
| 尺寸         | 36.0*20.0mm                |

#### 2. 中央处理单元

+  pyAI-K210 是由 01Studio 设计研发，基于嘉楠科技边缘计算芯片 K210（RSICV 架构，64 位双核）方案的一款开发板，其接口兼容 MicroPython 的 pyBoard，该芯片带有独立FPU的双核处理器，64位的CPU位宽，8M片内SRAM，400M可调标称频率，支持乘法、除法和平方根运算的双精度FPU；它还板载128Mbit高速大容量Flash、高速USB转串口芯片CH552、RGB LED、MEMS麦克风、24pin DVP摄像头接口、24pin 8bit MCU LCD接口，而这一切都设计在一块53.3mm 25.4mm的电路板上。该款产品的主要特点是RISC架构、高性能、低价格、AI概念。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.3.1 K210芯片主图.png" alt="图4.3.1 K210芯片主图" style="zoom:80%;" />

+  **KPU**是K210内部一个神经网络处理器，它可以在低功耗的情况下实现卷积神经网络计算，实时获取被检测目标的大小、坐标和种类，对人脸或者物体进行检测和分类。KPU具备以下几个特点:支持主流训练框架按照特定限制规则训练出来的定点化模型；对网络层数无直接限制，支持每层卷积神经网络参数单独配置，包括输入输出通道数目、输入输出行宽列高；支持两种卷积内核11和3x3；支持任意形式的激活函数；实时工作时最大支持神经网络参数大小为55MiB到59MiB；非实时工作时最大支持网络参数大小为(Flash容量软件体积)。
+  **接口方式**：pyAI-K210通过串口烧写程序和通信，通过安装USB转串口驱动，将开发板通过MicroUSB数据线连接到电脑。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.3.2 K210电脑连接方式.png" alt="图4.3.2 K210电脑连接方式" style="zoom:80%;" />

#### 3. 输出单元

##### 1）LCD显示单元

+  显示模块使用8位并口总线接口通信，由ST7789V和NS2009芯片驱动的2.8寸LCD液晶显示屏。该显示屏位TFT色域的电阻屏，通过24Pin-0.5mmFPC座连接驱动板，具有可操作性强，便捷可视化的优点，且监测结果实时反馈在显示屏上能够方便测试人员调试功能，且显示屏功耗较低可直接由驱动板供电，无需另外考虑屏幕供电问题。
+ **接口方式**：使用24P排线接入K210主板。
+ **实现方式**：由FPC排线具体控制。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.4.1  LCD显示屏.png" alt="图4.4.1  LCD显示屏" style="zoom:80%;" />

| 驱动芯片 | ST7789V+NS2009    |
| -------- | ----------------- |
| 颜色参数 | TFT               |
| 分辨率   | 240*320           |
| 屏幕尺寸 | 3.3V              |
| 通信方式 | 8位并口总线       |
| 接口定义 | 24Pin-0.5mm FPC座 |
| 整体尺寸 | 7.0*5.0cm         |

##### 2）音频模块

+ 音频模块使用标准I2S数字接口通信，功放端为两路3W的D类功放PAM8403，PAM8403是一颗输出功率为3万特的D类音制功率放大器IC，它具有谐波失直低，噪声串扰小的特点伸对声音的重放得到较好的音质。采用新型无耦合输出及无低通滤波电路之架构使其可直接驱动喇叭降低了整个方案成本及PCB空间的占用。在相同的外围元器件个数下，D类功放IC PAM8403比甲类功放的效率要好得多，这样就延长了电池的续航力，是携便式设备的理想选择。该模块同时支持标准3.5MM音频接口输出，可连接外置扬声器。
+ **接口方式**：使用标准I2S数字接口通信。
+ **实现方式**：将音频模块安装好后，K210一共有三个I2S设备，每个设备一共有4个通道，在使用之前需要对引脚进行映射管理，在代码中注册音频使能IO和音频控制IO，用上一级的监测结果控制wav格式音频文件的播放。将wav格式的四种不同音频文件保存在SD卡中，使用函数在判断结束后调用对应的音频模块。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图 3.10音频模块.png" alt="图 3.10音频模块" style="zoom:60%;" />

| 模块方案 | PT8211+PAM8403                    |
| -------- | --------------------------------- |
| 控制方式 | I2S                               |
| 功放类型 | D类                               |
| 输出功率 | 2路3W                             |
| 整体尺寸 | 3.0*2.5cm                         |
| 其他     | 标准3.5mm音频接口输出（自动切换） |

##### 3）舵机模块

+ 舵机又叫伺服电机，是一个可以旋转特定角度的电机，可转动角度通常是90°、180°和 360°。舵机常用在机器人身上或需要灵活转动的部件上，我们使用舵机来模拟闸门的开关状态。
+ **接口方式**：使用IO排线接入通信。
+ **实现方式**：180°舵机的控制需要一个 20ms 左右的时基脉冲，该脉冲的高电平部分一般为 0.5ms-2.5ms 范围内的角度控制脉冲部分，总间隔为 2ms，对应电机转角为 -90°至 90°。在核心开发板K210上安装拓展版，将伺服电机的排线接在扩展版的17、35、33、34针脚上，可以实现通过K210开发板对舵机的控制。通过板载程序对口罩佩戴的判断结果和测温结果做出一个综合判断后，将结果传向舵机，控制闸门的开闭。导入封装好的PWM模块后，将各模块进行初始化。定义舵机驱动的函数，向函数中传入不同参数即可以实现使舵机旋转不同角度。

<img src="D:\disc_C_backup\PIC\博文所用\双创\图4.4.3 舵机模块1.png" alt="图4.4.3 舵机模块1" style="zoom:80%;" />

| 反应转速 | 0.12—0.13秒/60° |
| -------- | --------------- |
| 适用温度 | -30°---- + 60°  |
| 工作扭矩 | 1.6KG/CM        |
| 工作电压 | 3.5 – 6V        |
| 转角角度 | 180°            |
| 接口类型 | IO排线X1 --- X4 |

### 总体控制代码

```python
import os, sys
import sensor, image, time, lcd, utime # 此版本中_thread不能用
import KPU as kpu
import audio   # 创建audio对象
from Maix import I2S, GPIO   # 创建I2S对象(用于处理音频对象)
from fpioa_manager import fm
import mlx90614
from machine import I2C  # 创建I2C用来处理测温对象
from machine import Timer,PWM # 舵机相关模块


# =========全局参数=================
audio_list = ["/sd/audio/without_mask.wav", "/sd/audio/with_incorrect_mask.wav",
                    "/sd/audio/with_correct_mask.wav"]
start_audio = '/sd/audio/start.wav'

labels = ["without_mask", "with_incorrect_mask", "with_correct_mask"]
rectangle_colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]

anchors = [0.4624, 0.6407, 1.0504, 1.4755, 1.5644, 2.7494, 2.7246, 3.2987, 4.4157, 4.42]

model_addr="/sd/model/1000.kmodel"   # 模型存放地址

normal_temp = [34.5, 37.9]         # 正常温度区间
recognition_number = 10    # 确定身份需要识别的次数
offset = 3  # 偏移量，值越小，识别越严格
temp_cunt = 10000  # 测温计数超过30000次后认为测温失败，继续下次循环， 约16秒时间
start_background = "pics/logo.jpg"  # logo图片地址
model_load_error = "/sd/pics/model_load_error.jpg"  # 模型加载失败图片地址
get_temp_error = "/sd/pics/get_temp_error.jpg"



# =========设备初始化================
# lcd初始化
lcd.init(type=1)
lcd.clear(lcd.WHITE)
#lcd.rotation(1)  # 屏幕旋转

# 摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 像素格式彩色RGB
sensor.set_framesize(sensor.QVGA)  # 设置帧的大小为QVGA（320*240）
# sensor.set_vflip(1)                 # 将摄像头设置成后置方式（所见即所得）
sensor.set_windowing((224,224))  # 设置窗口ROI：在要处理的图像中提取出的要处理的区域。
sensor.set_hmirror(False)   # 设置摄像头水平镜像：enable: 1 表示开启水平镜像 0 表示关闭水平镜像
sensor.set_vflip(False)   # 设置摄像头垂直翻转：enable: 1 表示开启垂直翻转 0 表示关闭垂直翻转
sensor.run(0)  # 图像捕捉功能：enable: 1 表示开始抓取图像 0 表示停止抓取图像

# 音频模块初始化
fm.register(32, fm.fpioa.GPIO1, force=True)
wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
wifi_en.value(1)
fm.register(34, fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
fm.register(33, fm.fpioa.I2S0_WS, force=True)
wav_dev = I2S(I2S.DEVICE_0)
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT,
                        cycles = I2S.SCLK_CYCLES_32, align_mode = I2S.RIGHT_JUSTIFYING_MODE)

# 红外测温初始化
i2c = I2C(I2C.I2C0,freq=100000,sda=6, scl=7)     #引进测温通信I2C

# 舵机模块初始化
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
S1 = PWM(tim, freq=50, duty=0, pin=17)   # PWM 通过定时器配置，接到 IO17 引脚



# =============定义控制函数======================
# 音频函数
def audio_play(audio_addr):
    # init audio
    player = audio.Audio(path=audio_addr)
    player.volume(100)

    # read audio info
    wav_info = player.play_process(wav_dev)

    # config i2s according to audio info
    wav_dev.set_sample_rate(wav_info[1])

    # loop to play audio
    while True:
        ret = player.play()
        if ret == None:
            print("format error")
            break
        elif ret == 0:
            break
    time.sleep_ms(100)  # 结束后延时100ms
    player.finish()


# 加载单张图片
def display_signal_pic(pic_addr):
    img = image.Image(pic_addr, copy_to_fb=True)
    lcd.display(img)


# 画框并标注度
def display_rectangle_str(position, label, color, scale, img):
    img.draw_rectangle(position, color=color, thickness=4)   # 画框
    img.draw_string(position[0], position[1], label, scale=scale, color=color)  #标明类别


# 加载模型
def load_model(model_addr, anchors):
    task = None  #清空
    task = kpu.load(model_addr)   #加载sd卡中的kmodel模型
    kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]初始化yolov2网络，识别可信概率为0.5（50%）
    return task


# 红外测温
def get_temp(i2c):
    cunt = 0
    temp = 0.0
    while temp < normal_temp[0]:  # 当测得的温度一直小于最低温度值时则一直测温
        try:
            temp = mlx90614.MLX90614(i2c).ObjectTemp()  # 运行测温模块返回温度值
            cunt += 1
            if cunt == temp_cunt:
                return None
        except:
            display_signal_pic(get_temp_error)
            time.sleep_ms(10000)
            # 退出程序
            sys.exit()

    return round(temp, 2)


# 舵机控制函数
def Servo(servo,angle):
    S1.duty((angle+90)/180*10+2.5)



# =========流程控制函数===========
# 开机界面
def start_up():
    display_signal_pic(start_background)
    audio_play(start_audio)


# 判断最终是否是一个确定状态
def determine_final_state(obj, state_flag, state_sum, check_sum):
    if obj.classid() == 1:   # 顺序映射
        classid = 2
    elif obj.classid() == 2:
        classid = 1
    else:
        classid = 0
    state_flag.append(classid)
    if len(state_flag) >= recognition_number:
        state_sum = sum(state_flag)
        if state_sum < offset:     # 如果和小于offset，则表明都是第一类，即classid为0
            check_sum = state_sum
            state_flag = []
            state_sum = 0
            return True, state_flag, state_sum, check_sum
        elif state_sum > (recognition_number-offset) and state_sum < (recognition_number+offset):
            check_sum = state_sum
            state_flag = []
            state_sum = 0
            return True, state_flag, state_sum, check_sum
        elif state_sum > (2*recognition_number-offset):
            check_sum = state_sum
            state_flag = []
            state_sum = 0
            return True, state_flag, state_sum, check_sum
        else:
            state_flag = []
            state_sum = 0
    return False, state_flag, state_sum, check_sum


# 舵机开门-延时-关门
def servo_control():
    """开始舵机处于复位状体，也就是关门状态"""
    Servo(S1, -90)
    time.sleep_ms(3000)
    Servo(S1, 0)


# ==========正式控制流程=============
# 开机画面
start_up()

# 摄像头开始拍摄
sensor.run(1)

# 舵机复位
Servo(S1, 0)  # 舵机复位成关门状态

# 加载模型
try:
    task = load_model(model_addr, anchors)
except:
    display_signal_pic(model_load_error)
    time.sleep_ms(10000)
    # 退出程序
    sys.exit()

state_flag = []   # 状态标志列表
state_sum = 0  # 状态和
check_sum = 0  # 记录每次判断的状态和，将清零前的最后一次用作状态的判断
flag = True
while flag:
    # 摄像头抓取图像
    img = sensor.snapshot()
    # 调用模型识别
    objects = kpu.run_yolo2(task, img)
    if objects:
        # 设只检测出一个脸，所以取objects中第一个元素
        obj = objects[0]
        state, state_flag, state_sum, check_sum = determine_final_state(obj, state_flag, state_sum, check_sum)
        if state:
            classid = int(check_sum / recognition_number + 0.5)  # 取整数
            display_rectangle_str(position=obj.rect(), label=labels[classid],
                            color=rectangle_colors[classid], scale=2, img=img)
            lcd.display(img)
            # 播放声音
            audio_play(audio_list[classid])
            if classid == 2:   # 即正确佩戴口罩
                # 测温部分
                temp = get_temp(i2c)
                if temp == None:
                    img.draw_string(50, 200, 'get temop failed!!!', scale=2, color=(255, 0, 0))  # 测温失败，显示为红色
                    lcd.display(img)
                    time.sleep_ms(500)
                elif temp >= normal_temp[1]:
                    img.draw_string(140, 200, str(temp)+" C", scale=2, color=(255, 0, 0))  # 温度较高，显示为红色
                    lcd.display(img)
                    time.sleep_ms(300)
                    audio_play('audio/abnormal_temp.wav')
                else:
                    img.draw_string(140, 200, str(temp)+" C", scale=2, color=(0, 255, 0))   # 温度正常显示为绿色
                    lcd.display(img)
                    audio_play('audio/normal_temp.wav')
                    # 舵机符合条件后转动
                    servo_control()
                continue
    else:
        state_flag = []
    lcd.display(img)
```

其中模型文件、音频文件和各种提示图片需要自己准备。将各种文件存到SD卡中，插在K210开发板上即可运行

### 创新之处和遇到问题的解决

#### 1. 研发过程中遇到的问题

##### 1）测温模块在程序运行中一直返回温度值，是测得的环境温度

**解决办法**：经过分析后可得在程序的循环中，测温模块一直在测量温度。将控制程序改为只有在识别到正确佩戴口罩后才会测量温度。设定[34.5 37.9]的温度区间，低于最低值是认为测得的是环境温度，测温失败；高于该区间的最大值后认为体温异常，播放声音提醒。并且在5秒内没有测得大于温度区间最小值的温度后，视为放弃测温，程序进入下一次循环。

##### 2） 口罩识别模型会对摄像头采集的每一帧图像进行识别，如果对模型输出的每一个预测结果做出反应的话，会造成系统过于混乱

**解决办法**：我们在发现这个问题后，认为模型对摄像头采集的每一帧进行预测并作出后续反应的话，会造成系统混乱，因为模型有小概率会识别不稳定。经过几天的仔细思考，发现可以利用模型识别的累积效果，引入状态列表和状态和变量，将模型识别10的结果存入状态列表中，并在状态列表长度为10时计算状态和。模型识别结果0为without_mask, 1为with_correct_mask, 2为with_incorrect_mask. 若状态和小于3，则认为这10次中多数都是without_mask，识别为正确佩戴口罩；若状态和在7到13之间，则认为10次中多数都是with_correct_mask，识别为正确佩戴口罩；若状态和大于17，则认为10次中多数是with_incorrect_mask，识别为口罩佩戴不正确。

​	经过这样的累计效果后，系统可以正常工作，识别精度也有提升，但是正确佩戴口罩和口罩佩戴不正确会识别错误，分析原因是，由于模型预测结果2被认为是with_incorrect_mask，所以10次中有少数的with_incorrect_mask和多数的with_correct_mask也会被判定为口罩配得不正确。将模型预测结果1改为with_incoeerct_mask，2改为with_correct_mask后，这个问题有很大改善，识别精度进一步提高。

##### 3） 由于K210开发板可用接口有限，在正常的插上测温模块后就不能插舵机模块了。

**解决方法**：比较容易的解决方案是再买一个pybase拓展板来接舵机，但是由于财力有限，不能支付得起拓展板的钱。在深入研究测温模块的排线结构后发现测温模块可以不用全部接在K210开发板上，只需4条线接入即可，这样给舵机模块留下了接口。可以把测温模块固定到其他地方，用几根杜邦线就把测温模块和舵机模块接到K210开发板上。



#### 2. 测试阶段遇到的问题

##### 1） 语音播报模块在播放完音频后会有一声比较短暂刺耳的爆音

**解决方法**： 在语音播报的测试程序中，播放完声音序列后加上100ms的短暂延时，使程序不要过快的结束掉，可以解决爆音问题

##### 2） 模型对测试数据集预测效果不好，准确率较低

**解决方法**：经过排查，是测试程序中anchors值不对，anchors需要有训练时的数据集计算得到。在更改anchors值后，测试精度有了很大提高

### 不足待改进之处

#### 1. 弱光条件下识别准备率有待提升

##### 1） 原因

受摄像头硬件性能限制，在弱光条件下摄像头采集的图像较模糊，使模型不能正确判断口罩佩戴情况，造成识别正确率下降和延迟上升。

##### 2） 建议改进措施

+ 更换拍摄质量更好、像素更高的摄像头

+ 在摄像头附近增加补光灯和光敏传感器，在光敏传感器检测到光照条件低于一定阈值后，在识别口罩的时候打开补光灯补光；在光照良好的情况下不开补光灯。

#### 2. 远距离识别准确率不高

##### 1） 原因

受摄像头设置所限，在距离较远时采集的图像模糊，使模型不能正确判断口罩佩戴情况，造成识别正确率下降和延迟上升。

##### 2） 建议改进措施

+ 更换拍摄质量更好、像素更高的摄像头

#### 3. 测温模块精度不高

##### 1） 原因

+ 财力有限，并且目前K210只能支持这样的测温模块，导致测温模块质量不好，精度不高，目前为 +- 0.3℃

##### 2） 建议改进措施

+ 有条件就更换精度更高的测温模块，
+ 或者自己根据K210的引脚接口设计一款测温模块

### 产品图

#### 1. 内部结构

<img src="D:\disc_C_backup\PIC\博文所用\双创\产品内部结构.jpg" alt="产品内部结构" style="zoom:67%;" />

#### 2. 产品外观图

<img src="D:\disc_C_backup\PIC\博文所用\双创\产品外观.jpg" alt="产品外观" style="zoom: 67%;" />

### 参考资料

+ [《MicroPython从0到1》基于K210平台](https://www.aliyundrive.com/s/hwAWwdLGmvT)
+ [固件及开发软件IDE下载]([下载站 - Sipeed](http://cn.dl.sipeed.com/MAIX/MaixPy/ide/_/v0.2.4))
+ [官方文档]([MaixPy 文档简介 - Sipeed Wiki](https://wiki.sipeed.com/soft/maixpy/zh/index.html))
+ [Sipeed MaixHub – sipeed AI 模型平台](https://www.maixhub.com/)

### 开源声明

本文档及全部资料已经在Github开源，链接为：https://github.com/the-light011/Face-Mask-detction-DeepLearning

采用**[Apache License 2.0](https://github.com/the-light011/Face-Mask-detction-DeepLearning/blob/main/LICENSE)**开源协议




