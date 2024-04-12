# FINAL PROJECT: How to easily find my Uber
## Introduction
It is not easy to find the Uber I called or find my own vehicle in very crowded places such as LAX or large shopping malls.
Moreover, if I have low vision or am a traveler, it will be even more difficult to find my vehicle.

So, I created a way to communicate with the vehicle (Monitor) using ultrasonic sensors and pressure sensors as remote control to more easily find and find the Uber I called.

So, when the Uber I called comes near me, I put my phone in the remote control holder that contains the pressure sensor. Afterwards, when I get close to the vehicle, the Ultrasonic sensor measures the distance, and the music gets louder and louder in my Uber vehicle (Monitor) (and the colors I choose change and are expressed along with the sound), it making it easier to find my Uber for me. 

From Now on, you can find easier your Uber too.

![image](img/1.png)



![image](img/5.png)


![image](img/6.png)

##
## Implementation
### Hardware - material & wiring
I used:

- 1 Atom s3 lite board
- 1 Ultrasonic sensor
- 1 Pressure sensor

![image](img/Flowchart.jpg)

![image](img/11.jpg)

![image](img/12.jpg)

![image](img/13.jpg)

![image](img/14.jpg)

![image](img/15.jpg)

##
## Firmware - hardware
Pressure sensor setup:

``` py
adc = ADC(Pin(PRESSURE_SENSOR_PIN))
adc.atten(ADC.ATTN_11DB)
```

Define the maximum and minimum distances for the ultrasonic sensor:
``` py
MAX_DISTANCE_CM = 400
MIN_DISTANCE_CM = 2  
```

Trigger the ultrasonic sensor:

``` py
 trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
```

Calculate the distance in cm (speed of sound is 0.0343 cm/µs, so distance = timepassed * 0.0343/2):
``` py
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
```

Read the value from the pressure sensor; Call the function to read the distance from the ultrasonic sensor; Print the value to monitor the value, if the value is right, if the connection is stable:
``` py
 while True:
        pressure_val = adc.read()
        distance_val = read_ultrasonic()

        if distance_val is not None:
            print("{},{}".format(distance_val, pressure_val))
        else:
            print("Distance invalid,{}".format(pressure_val))

        time.sleep(0.5)
```


##
##Firmware - software
Add 2 videos to the software and hide default video elements on screeen:
``` py
 createCanvas(windowWidth, windowHeight);
    vid1 = createVideo("video1.mp4");
    vid2 = createVideo("video2.mp4");

    vid1.size(windowWidth, windowHeight);
    vid2.size(windowWidth, windowHeight);

    vid1.hide();
    vid2.hide(); 
```

Use conditional operator to determine which video should play based on pressure sensor value, if value is greater than 4000, play video 1; if value is less than 4000, toggle to video 2; Besides that, check if a transition is not already happening:
``` py
 let newVideo = (pressure > 4000) ? vid1 : vid2;
    if (newVideo !== currentVideo && !isTransitioning) {
        nextVideo = newVideo;
        isTransitioning = true;
        nextVideo.time(0);
        nextVolume = 0;
    }
```


Volume fade in and out during transition:
``` py
  currentVolume = max(0, currentVolume - volumeTransitionSpeed);
  nextVolume = min(1, nextVolume + volumeTransitionSpeed);
```

Video fade in and out during transition:
``` py
  fade += 2;
```

``` py
  if (fade >= 255) {
            fade = 0;
            currentVideo.hide();
            currentVideo = nextVideo;
            nextVideo = null;
            isTransitioning = false;
            currentVolume = nextVolume;
            nextVolume = 0;
```

``` py
 tint(255, 255 - fade);
    image(currentVideo, 0, 0, windowWidth, windowHeight);
    if (nextVideo) {
        tint(255, fade);
        image(nextVideo, 0, 0, windowWidth, windowHeight);
```

##
##Change volume based on the distance (ultrasonic value):

``` py
  if (distance >= 100) {
            currentVolume = 0;
        } else if (distance <= 50) {
            currentVolume = 1;
        } else {
            currentVolume = map(distance, 50, 100, 1, 0);
        }
```

##
##Integrations
I created two motion clips by using after effects in this project and uploaded them locally. So that I can directly call them in the software.

