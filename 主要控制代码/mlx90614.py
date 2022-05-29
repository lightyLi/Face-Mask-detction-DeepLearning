'''
要求：
i2c = SoftI2C(scl=x, sda=x)
temp = mlx90614.MLX90614(i2c)
temp.ObjectTemp() #返回物体温度
temp.AmbientTemp() #返回周围温度
作者：01Studio用户：jd3096
技术社区：bbs.01studio.cc
'''

import ustruct,utime
from micropython import const

_TA_ADDRESS = const(0x06)    
_TOBJ1_ADDRESS = const(0x07)
_TOBJ2_ADDRESS = const(0x08)  

class MLX90614:
    def __init__(self, i2c):
        self.i2c = i2c
        self.address = 0x5a

    def readdata(self, register):
        try:
            data = self.i2c.readfrom_mem(self.address, register, 2)
            return ustruct.unpack('<H', data)[0]
        except:
            pass

    def read_temp(self, register):
        temp = self.readdata(register)
        temp=temp/50-273.15
        return temp

    def AmbientTemp(self):
        return self.read_temp(_TA_ADDRESS)

    def ObjectTemp(self):
        return self.read_temp(_TOBJ1_ADDRESS)
