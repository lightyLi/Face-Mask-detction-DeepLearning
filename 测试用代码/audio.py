from Maix import I2S, GPIO
import audio
from fpioa_manager import *
import time

fm.register(32, fm.fpioa.GPIO1, force=True)
wifi_en=GPIO(GPIO.GPIO1, GPIO.OUT)
wifi_en.value(1)
fm.register(34, fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
fm.register(33, fm.fpioa.I2S0_WS, force=True)


# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_0)
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                   cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)

def audio_play(audio_addr):
    # init audio
    player = audio.Audio(path=audio_addr)
    player.volume(40)

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
            print("end")
            break

    time.sleep_ms(100)
    player.finish()


def func(i):
    print(i)

i = 0
audio_list = ["/sd/1.wav", "/sd/2.wav", "/sd/3.wav"]
while True:
    i += 1
    audio_play(audio_list[i])
    if i == 3:
        i = 0

