import mlx90614, time
from machine import I2C  # 创建I2C用来处理测温对象

# 红外测温初始化
i2c = I2C(I2C.I2C0,freq=100000,sda=6, scl=7)     #引进测温通信I2C

# 获取测温值
def get_temp(i2c):
    temp = mlx90614.MLX90614(i2c)   # 运行测温模块返回温度值
    return round(temp.ObjectTemp(), 2)

normal_temp = [34.5, 38.0]
def get_temp(i2c):
    cunt = 0
    temp = 0.0
    while temp < normal_temp[0]:  # 当测得的温度一直小于最低温度值时则一直测温
        temp = mlx90614.MLX90614(i2c).ObjectTemp()  # 运行测温模块返回温度值
        cunt += 1
        if cunt == 30000:
            return '测温失败'
    return round(temp, 2)
temp = get_temp(i2c)

print(temp)


