import os, sys, io
import M5
from M5 import *
from hardware import *
import time



Title0 = None
pin8 = None


button_value = None


def setup():
  global Title0, pin8, button_value

  M5.begin()
  Title0 = Widgets.Title("Hi Romey", 3, 0xFFFFFF, 0xeaa5ff, Widgets.FONTS.DejaVu18)

  Title0.setText('button input')
  pin8 = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP)


def loop():
  global Title0, pin8, button_value
  button_value = pin8.value()
  M5.update()
  if button_value == 0:
    Title0.setText('button on')
  else:
    Title0.setText('romey off')
  time.sleep(1)


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

