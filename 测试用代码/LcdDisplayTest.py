import lcd, image
import os
import  time


print(os.listdir())

lcd.init(type=1)
lcd.clear(lcd.WHITE)
lcd.rotation(3)

img_addr = 'pics/vegetable.jpg'
img  = image.Image(img_addr, copy_to_fb=True)
#img  = image.Image(size=(320, 240))
img.draw_string(50, 120, "welcome!", color=(255, 0, 0), scale=3)  #255，255，255白色

lcd.display(img)



# 显示纯色背景和文字， 用于显示错误和警告信息
def display_purepic_str(position, string, color, scale):
    img = image.Image(size=(320, 240), color = (255, 200, 0))
    img.draw_string(position[0], position[1], string, color=color, scale=scale)
    lcd.display(img)

# 显示背景图片和文字, 用于开机欢迎界面
def display_pic_str(position, string, color, scale, pic_addr):
    img = image.Image(pic_addr, copy_to_fb=True)
    img.draw_string(position[0], position[1], string, color=color, scale=scale)
    lcd.display(img)



# 画框并标注
def display_rectangle_str(position, string, color, scale, img, temp):
    img.draw_rectangle(position[0], position[1],color=color,thickness=4)   # 画框
    img.draw_string(position[0], position[1], string, scale=scale, color=color)  #标明类别
    img.draw_string(0, 200, '%.2f' %temp, scale=2, color=(255, 0, 0))   # 显示温度




display_pic_str(position=[1, 2], string='KALLO!!!', color=(0, 200, 255), scale=3, pic_addr='pics/vegetable.jpg')

time.sleep_ms(10000)





