# using ADC input to control servo movement
# NOTE: servo.py file should be saved to hardware first

import os, sys, io
import M5
from M5 import *
from hardware import *
import time
from servo import Servo  # import servo.py

title0 = None
label0 = None
servo = None
adc1 = None

def setup():
  global title0, label0, servo, adc1
  M5.begin()
  # display title ("title text", text offset, fg color, bg color, font):
  title0 = Widgets.Title("adc servo", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  # display label ("label text", x, y, layer number, fg color, bg color, font):
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  # configure servo on pin 38:
  servo = Servo(pin=38)
  servo.move(90)  # stop the servo
  # initialize analog to digital converter on pin 1:
  adc1 = ADC(Pin(1), atten=ADC.ATTN_11DB)
  
# function to map input value range to output value range:
def map_value(in_val, in_min, in_max, out_min, out_max):
  out_val = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
  if out_val < out_min:
    out_val = out_min
  elif out_val > out_max:
    out_val = out_max
  return int(out_val)

def loop():
  global label0
  M5.update()
  # read 12-bit ADC value (0 - 4095 range):
  adc1_val = adc1.read()
  # convert ADC value from 0-4095 range to 0-180 range:
  servo_val = map_value(adc1_val, in_min=0, in_max=4095, out_min=0, out_max=180)
  print('servo_val =', servo_val)
  # move servo using servo_val as input:
  servo.move(servo_val)
  # display servo value on label0:
  label0.setText(str(servo_val))
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
