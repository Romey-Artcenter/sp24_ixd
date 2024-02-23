import os, sys, io
import M5
from M5 import *
from hardware import *  # import RGB and other hardware
import time
import math

title0 = None
label0 = None
label1 = None
label2 = None

imu_val = None
rgb = None
rainbow_offset = 0

def setup():
  global title0, label0, label1, label2
  global rgb

  M5.begin()
  title0 = Widgets.Title("IMU test", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  label1 = Widgets.Label("--", 3, 40, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  label2 = Widgets.Label("--", 3, 60, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  
  # initialize RGB LED strip on pin 38 (AtomS3 PortABC red connector) with 30 pixels:
  rgb = RGB(io=38, n=30, type="SK6812")
  # turn off RGB LEDs (fill with black):
  rgb.fill_color(0x000000)

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

def rgb_rainbow():
  global rgb, rainbow_offset
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

def loop():
  global title0, label0, label1, label2
  global imu_val
  M5.update()
  
  # read the IMU accelerometer values:
  #3개의 위치 imu_val
  imu_val = Imu.getAccel()
  #X axis acceleration is first item
  imu_x_val = imu_val[0]
  imu_y_val = imu_val[1]
  imu_z_val = imu_val[2]
  
  # print all IMU values (X, Y, Z):
  print(imu_val)
  # print the first IMU value (X) only:
  #print('acc x:', imu_val[0])
  #print('acc y:', imu_val[1])
  #print('acc x:', imu_x_val)
  #print('acc y:', imu_y_val)
  
  #display right or left according to X axis tilt:
#   if imu_x_val < -0.5:
#     label0.setText('Right')
#   elif imu_x_val > 0.7:
#     label0.setText('Left')
#   else:
#     label0.setText('X-wrong')
#   
#   #display right or left according to Y axis tilt:
#   if imu_y_val < -0.5:
#     label0.setText('DOWN')
#   elif imu_y_val > 0.5:
#     label0.setText('UP')
#   else:
#     label0.setText('Y-wrong')
#
  if imu_z_val < -0.25:
    label0.setText('Wrong')
    rgb.fill_color(0xff0000)  # fill all pixels red
    time.sleep_ms(100)
  elif imu_z_val > 0.25:
    label0.setText('Wrong')
    rgb.fill_color(0xff0000)  # fill all pixels red
    time.sleep_ms(100)
  else:
    label0.setText('OK!')
    rgb_rainbow()
  
  
  # format each IMU value with 2 points precision:
  #imu_str = 'acc x: {:0.2f}'.format(imu_val[0])
  #label0.setText(imu_str)
  #imu_str = 'acc z: {:0.2f}'.format(imu_z_val)
  #label1.setText(imu_str)
  #imu_str = 'acc z: {:0.2f}'.format(imu_val[2])
  #label2.setText(imu_str)
  
  


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


