# display changing hues (rainbow colors) on RGB LED strip

import os, sys, io
import M5
from M5 import *
from hardware import *
import time
import math

title0 = None
rgb = None
rainbow_offset = 0

def setup():
  global title0, rgb
  M5.begin()
  # initialize dispaly title and label:
  title0 = Widgets.Title("RGB rainbow", 0, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  # initialize RGB LED strip on pin 38 (AtomS3 PortABC red connector) with 30 pixels:
  rgb = RGB(io=38, n=30, type="SK6812")
  # turn off RGB LEDs (fill with black):
  rgb.fill_color(0x000000)
  
# function to combine r, g, b color components into one color value:
def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color

# function to map input value range to output value range:
def map_value(in_val, in_min, in_max, out_min, out_max):
  out_val = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
  if out_val < out_min:
    out_val = out_min
  elif out_val > out_max:
    out_val = out_max
  return int(out_val)

# function to combine hue, saturation, brightness into one color value:
def hsb_to_color(h, s, v):
    h = float(h)/255.0
    s = float(s)/255.0
    v = float(v)/255.0
    
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]
    r = int(255 * r)
    g = int(255 * g)
    b = int(255 * b)
    rgb_color = (r << 16) | (g << 8) | b
    return rgb_color

def loop():
  global label0, rgb
  global rainbow_offset
  M5.update()
  # show color rainbow:
  for i in range(30):
    # hue based on pixel index:
    #hue = map_value(i, 0, 30, 0, 255)
    # hue based on pixel index and rainbow offset:
    index = (i + rainbow_offset) % 30
    hue = map_value(index, 0, 30, 0, 255)
    color = hsb_to_color(hue, 255, 255)
    rgb.set_color(i, color)
  rainbow_offset += 1
  time.sleep_ms(50)

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


