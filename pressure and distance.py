from machine import Pin, ADC
import time

PRESSURE_SENSOR_PIN = 1
TRIG_PIN = 39
ECHO_PIN = 38

MAX_DISTANCE_CM = 400
MIN_DISTANCE_CM = 2  

adc = ADC(Pin(PRESSURE_SENSOR_PIN))
adc.atten(ADC.ATTN_11DB)

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def read_ultrasonic():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    while echo.value() == 0:
        signaloff = time.ticks_us()

    while echo.value() == 1:
        signalon = time.ticks_us()

    timepassed = signalon - signaloff
    distance_cm = (timepassed * 0.017)

    if distance_cm < MIN_DISTANCE_CM or distance_cm > MAX_DISTANCE_CM:
        return None
    else:
        return distance_cm

try:
    while True:
        pressure_val = adc.read()
        distance_val = read_ultrasonic()

        if distance_val is not None:
            print("{},{}".format(distance_val, pressure_val))
        else:
            print("Distance invalid,{}".format(pressure_val))

        time.sleep(0.5)
except KeyboardInterrupt:
    print("STOP")
