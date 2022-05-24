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

