# beginner program for M5Stack AtomS3 based on uiflow2 code structure

import os, sys, io
import M5
from M5 import *
from hardware import *
import time
from servo import Servo #import servo.py

title0 = None
label0 = None
servo = None

def setup():
  global title0, label0, servo
  M5.begin()
  # display title ("title text", text offset, fg color, bg color, font):
  title0 = Widgets.Title("TITLE", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  # display label ("label text", x, y, layer number, fg color, bg color, font):
  label0 = Widgets.Label("label", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  #configure servo on pin 38
  servo = Servo(pin=38)
  servo.move(90)
  servo.move(100)
  
def loop():
  M5.update()
  #move servo slowly counter-clockwise
  servo.move(100)
  time.sleep(1) 
  #move fast clockwise
  servo.move(120)
  time.sleep(1)
  #move slowly clockwise
  servo.move(87)
  time.sleep(1)
  #move fast clockwise
  servo.move(50)
  time.sleep(1)
  #stop servo:
  servo.move(90)
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
