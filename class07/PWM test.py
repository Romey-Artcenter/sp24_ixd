# using the input function to update AtomS3 display label

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

title0 = None
label0 = None
pwm1 = None

def setup():
  global title0, label0, pwm1
  M5.begin()
  # display title ("title text", text offset, fg color, bg color, font):
  title0 = Widgets.Title("input test", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  # display label ("label text", x, y, layer number, fg color, bg color, font):
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  #initialize PWM on pin with frequency and duty cycle values:
  #pwm1 = PWM(Pin(1), freq=20000, duty=512)
  
  pwm1 = PWM(Pin(38))
  pwm1.duty(75) #75가 멈추는 0 구간, 75보다 낮으면 반대방향으로 돌고, 75보다 높으면 시계방향으로 돔, 200이 max속도
  pwm1.freq(50)


def loop():
  global pwm1
  M5.update()
  # wait for input and then assign it to input_str variable:
  input_str = input('inout servo duty cycle value: ')
  print('received:', input_str)
  #update pwm duty cycle input value
  pwm1.duty(int(input_str)) 
  # display the received input on label0:
  label0.setText(input_str)
  time.sleep_ms(100)
  
if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
