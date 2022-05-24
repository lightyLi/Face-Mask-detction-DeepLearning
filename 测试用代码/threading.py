import _thread
import time



def func1(name):
    while True:
        print("Hello World")
    time.sleep(1)

def func2(name):
    while True:
        print("你好")
    time.sleep(1)

_thread.start_new_thread(func1,("1",)) #开启线程 1，参数必须是元组
_thread.start_new_thread(func2,("2",)) #开启线程 2，参数必须是元组

while True:
    pass

