# Switching between 2 ways of mapping analog input to RGB LED output,
# using the screen button on AtomS3 to change program states

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

title0 = None
label0 = None
adc1 = None
adc1_val = None
rgb = None
program_state = 'RGB_FADE'

button_pin = None
button_value = 0
button_timer = 0

def setup():
  global label0, title0, adc1, rgb
  global button_pin
  M5.begin()
  # initialize dispaly title and label:
  title0 = Widgets.Title("my posture", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  # initialize analog to digital converter on pin 1:
  adc1 = ADC(Pin(1), atten=ADC.ATTN_11DB)
  # initialize RGB LED strip on pin 38 with 30 pixels:
  rgb = RGB(io=38, n=30, type="SK6812")
  # fill RGB LEDs with green:
  #rgb.fill_color(0x003300)
  # fill RGB LEDs with orange:
  rgb.fill_color(get_color(255, 60, 0))
  # initialize pin 41 (screen button on AtomS3 board) as input:
  button_pin = Pin(41, mode=Pin.IN)
  
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

def loop():
  global label0, title0
  global adc1, adc1_value, rgb
  global program_state
  global button_value, button_timer
  M5.update()
  # read 12-bit ADC value (0 - 4095 range):
  adc1_val = adc1.read()
  
  if program_state == 'RGB_FADE':
    # convert ADC value to 8 bits (0 - 255 range):
    adc1_val_8bit = map_value(adc1_val, in_min=0, in_max=4095, out_min=0, out_max=255)
    # print the ADC value:
    #print(adc1_val)
    print(adc1_val_8bit)
    # show ADC value on display label:
    label0.setText(str(adc1_val))
    # change red color in response to ADC value:
    red = adc1_val_8bit
    rgb.fill_color(get_color(red, 0, 0))
    time.sleep_ms(50)
    
  elif program_state == 'RGB_FILL':
    #rgb.fill_color(0x0000FF)  # fill with blue
    # convert ADC value to range of 30 pixels (0 - 29):
    adc1_val_30pix = map_value(adc1_val, 0, 4095, 0, 30)
    #rgb.fill_color(0x000000)  # fill all pixels black
    # fill pixels up to adc1_val_30pix with blue:
    for i in range(30):
      if i < adc1_val_30pix:
        rgb.set_color(i, 0x0000FF)
      else:
        rgb.set_color(i, 0x000000)
    print(adc1_val_30pix)
    time.sleep_ms(50)
  
  if time.ticks_ms() > button_timer + 500:
    button_timer = time.ticks_ms()  # update button_timer
    # read button value from button_pin:
    button_value = button_pin.value()
    if button_value == 0: # button was pressed
      if program_state == 'RGB_FADE':
        program_state = 'RGB_FILL'
      elif program_state == 'RGB_FILL':
        program_state = 'RGB_FADE'
      print('Good posture', program_state)
      title0.setText(program_state)
    

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
      print("Please straighten up your posture ")


