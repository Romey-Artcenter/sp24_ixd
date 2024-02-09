import os, sys, io
import M5
from M5 import *
from hardware import *



label0 = None
pin8 = None
pin1 = None


button_values = None


def setup():
  global label0, pin8, pin1, button_values

  M5.begin()
  label0 = Widgets.Label("INPUT_ROMEY", 0, 2, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

  pin8 = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP)
  pin1 = Pin(1, mode=Pin.OUT)


def loop():
  global label0, pin8, pin1, button_values
  M5.update()
  button_values = pin41.value()
  if button_values == 0:
    pin1.on()
  else:
    pin1.off()


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
