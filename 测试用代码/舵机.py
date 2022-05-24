from machine import Timer,PWM
import time

#PWM 通过定时器配置，接到 IO17 引脚
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
S1 = PWM(tim, freq=50, duty=0, pin=17)
'''
说明：舵机控制函数
功能：180 度舵机：angle:-90 至 90 表示相应的角度
 360 连续旋转度舵机：angle:-90 至 90 旋转方向和速度值。
 【duty】占空比值：0-100
'''

def Servo(servo,angle):
    S1.duty((angle+90)/180*10+2.5)
i = 0
while True:
    #-90 度
    Servo(S1, -90)
    time.sleep_ms(500)
    Servo(S1, 0)
    time.sleep_ms(500)
    Servo(S1, 90)
    time.sleep_ms(500)
    Servo(S1, -90)
    time.sleep_ms(500)
    print(i)

