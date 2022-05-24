import sensor, image, time, lcd

lcd.init(freq=15000000) #初始化 LCD
lcd.rotation(3)  # 旋转方向
sensor.reset() #复位和初始化摄像头，执行 sensor.run(0)停止。

# sensor.set_vflip(1) #将摄像头设置成后置方式（所见即所得）

sensor.set_pixformat(sensor.RGB565) # 设置像素格式为彩色 RGB565 (或灰色)
sensor.set_framesize(sensor.QVGA) # 设置帧大小为 QVGA (320x240)
#sensor.skip_frames(time = 2000) # 等待设置生效.
sensor.run(1)




img = sensor.snapshot() # 拍摄一个图片并保存.
lcd.display(img) # 在 LCD 上显示
