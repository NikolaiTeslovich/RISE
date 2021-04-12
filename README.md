<h1 align="center">
  The Rocket Lab Initiative — RISE
</h1>

<p align="center">
  <a href="https://github.com/NikolaiTeslovich/RISE/blob/main/LICENSE">
    <img alt="MIT license" src="https://img.shields.io/github/license/NikolaiTeslovich/RISE">
  </a>
</p>

Currently working on writing a program and designing a model rocket on which I will launch a Raspberry Pi Zero W with an array of sensors, which I've already designed.

Very much still *in progress*.

## To do

### Orient the STLs correctly!

- find appropriate camera resolution and framerate, [here's a helpful article](https://picamera.readthedocs.io/en/release-1.10/fov.html)
  - the spycam is the same as the picamera v1
- make script start on startup
- stop collecting data on landing, when the pressure data is no longer changing
- Should we truncate the data after a certain point to decrease file size? Like the hundreds or thousands place
  - Looking at the csv file, it seems that the digits repeat themselves, that there are only so many distinct messages

## Sensor payload & camera assembly

![SensorPayload](/resources/SensorPayload.jpeg)

### 3D printing
- STLs and Fusion 360 files located in the [files](/files) directory.
- Spacers were printed out of TPU
- Everything else was printed out of PLA at 215°C and 15% infill
  - Supports are only needed for the [SensorSkeleton](/files/SensorSkeleton.stl)

### Parts required
Just made of what I had lying around at the time. Feel free to change the hole sizes to fit your screw sizes through the included Fusion 360 files. Fusion 360 is free.

- 1x Raspberry Pi Zero W
- 1x PowerBoost 500C
- 1x LSM303DLHC
- 1x BMP338
- 1x [GNB 450mah 1s LiHV](https://www.amazon.com/PowerWhoop-Connector-Tinyhawk-Brushless-Inductrix/dp/B078Y3Y4ZZ/ref=sr_1_9?dchild=1&keywords=450mah+1s&qid=1617315333&sr=8-9) - it's what I use in my super small FPV drones
- 10x 5mm M2.5 screws - from some old computer hard-drives
- 1x 10mm M3 screw
- 1x small rubber band
- 1x printed parts (obviously)

### Things to keep in mind
The screws tap into the plastic, so **do not** over-tighten them. Other than that, assembly should be pretty self-explanatory.

Also, make sure that the battery polarity matches the polarity of the PowerBoost 500C JST connector. The one on the GNB 450mah 1s is reversed. Or else, this will happen.

  > *magic smoke will come out*.

![ShortedPowerBoost](/resources/ShortedPowerBoost.jpeg)
