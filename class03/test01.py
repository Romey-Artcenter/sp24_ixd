import os, sys, io
import M5
from M5 import *
from hardware import *
import time

pin_label = None
program_state_label = None

input_pin = None
input_value = 0
input_timer = 0
program_state = 'START'

def setup():
  global pin_label, program_state_label, input_pin

  M5.begin()
  pin_label = Widgets.Label("input", 5, 5, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  program_state_label = Widgets.Label("START", 5, 25, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  # initialize input on pin 41 (built-in button):
  #input_pin = Pin(41, mode=Pin.IN)
  # initialize input on pin 1 with pull up:
  input_pin = Pin(1, mode=Pin.IN, pull=Pin.PULL_UP)

def loop():
  global pin_label, program_state_label
  global input_value
  global input_timer
  global program_state
  M5.update()
  # check input every 500 ms (half second):
  if time.ticks_ms() > input_timer + 500:
    input_timer = time.ticks_ms()  # update button_timer
    input_value = input_pin.value()
    if input_value == 0:
      pin_label.setText('pin ON')
      if program_state == 'START':
        program_state = 'RUN'
        program_state_label.setText(program_state)
    else:
      pin_label.setText('pin OFF')
  
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
