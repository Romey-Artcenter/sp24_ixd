import os, sys, io
import M5
from M5 import *
import time
import math

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None

imu_val = None
imu_x_val = 0.0  # X-axis acceleration value now
imu_x_last = 0.0  # last X-axis acceleration value
imu_y_val = 0.0  # Y-axis acceleration value now
imu_y_last = 0.0  # last Y-axis acceleration value

def setup():
  global title0, label0, label1, label2, label3

  M5.begin()
  title0 = Widgets.Title("IMU test", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  label1 = Widgets.Label("--", 3, 40, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  label2 = Widgets.Label("--", 3, 60, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  label3 = Widgets.Label("--", 3, 80, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)

def loop():
  global title0, label0, label1, label2
  global imu_val, imu_x_val, imu_x_last, imu_y_val, imu_y_last
  M5.update()
  
  # read the IMU accelerometer values:
  imu_val = Imu.getAccel()
  # save the last X-axis acceleration value:
  imu_x_last = imu_x_val
  # update X-axis acceleration value:
  imu_x_val = imu_val[0]
  
  # save the last Y-axis acceleration value:
  imu_y_last = imu_y_val
  # update Y-axis acceleration value:
  imu_y_val = imu_val[1]
  
  # print all IMU values (X, Y, Z):
  print(imu_val)
  # print the first IMU value (X) only:
  #print('acc x:', imu_x_val)
  #print('acc y:', imu_y_val)
  
  # display RIGHT or LEFT according to X-axis tilt:
  if imu_x_val < -0.5:
    label0.setText('RIGHT')
  elif imu_x_val > 0.7:
    label0.setText('LEFT')
  else:
    label0.setText('')

  # display UP or DOWN according to Y-axis tilt:
  if imu_y_val < -0.5:
    label1.setText('DOWN')
  elif imu_y_val > 0.5:
    label1.setText('UP')
  else:
    label1.setText('')
    
  # display X MOTION according to change in X-axis:
  # absolute value of the difference between new and last X values:
  imu_x_diff = math.fabs(imu_x_val - imu_x_last)  
  #if (imu_x_val - imu_x_last > 0.5) or (imu_x_val - imu_x_last < -0.5):
  if imu_x_diff > 0.5:
    label2.setText('X MOTION')
  else:
    label2.setText('')
    
  imu_y_diff = math.fabs(imu_y_val - imu_y_last)  
  if imu_y_diff > 0.5:
    label3.setText('Y MOTION')
  else:
    label3.setText('')
    
  # format each IMU value with 2 points precision:
  #imu_str = 'acc x: {:0.2f}'.format(imu_val[0])
  #label0.setText(imu_str)
  #imu_str = 'acc y: {:0.2f}'.format(imu_val[1])
  #label1.setText(imu_str)
  #imu_str = 'acc z: {:0.2f}'.format(imu_val[2])
  #label2.setText(imu_str)
  
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
