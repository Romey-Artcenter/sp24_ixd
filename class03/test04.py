import os, sys, io
import M5
from M5 import *
from hardware import *



rgb2 = None


def setup():
  global rgb2

  M5.begin()
  rgb2 = RGB(io=2, n=10, type="SK6812")
  rgb2.fill_color(0xffff66)


def loop():
  global rgb2
  M5.update()


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

