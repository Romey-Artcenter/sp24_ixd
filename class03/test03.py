import os, sys, io
import M5
from M5 import *
from hardware import *
import time

rgb2 = None

i = None

def setup():
  global rgb2, i
  M5.begin()
  #initialize RGB LED strip on pin 2 with 10 pixels
  rgb2 = RGB(io=2, n=10, type="SK6812")

def loop():
  global rgb2, i
  M5.update()
  #fade in all pixel red color
  for i in range(100):
    rgb2.fill_color((i << 16) | (0 << 8) | 0)
    time.sleep_ms(20)
  #fade out all pixel red color
  for i in range(100):
    rgb2.fill_color((99-i << 16) | (0 << 8) | 0)
    time.sleep_ms(20)
  #fade in pixels' one by one with blue
  for i in range(10):
    rgb2.set_color(i, 0x0000FF)
    time.sleep_ms(200)


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

