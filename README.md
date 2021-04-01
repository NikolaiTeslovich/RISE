# RISE

Everything related to the *Penn State Rocket Lab Initiative*.

Currently working on writing a program and designing a model rocket on which I will launch a Raspberry Pi Zero W with an array of sensors.

Very much still *in progress*.

## Don't do this

![ShortedPowerBoost](/resources/ShortedPowerBoost.jpeg)

## To do

### Orient the STLs correctly!
### M2.5 definitively!
#### I got mine from an old hard drive lol

- find appropriate camera resolution and framerate, [here's a helpful article](https://picamera.readthedocs.io/en/release-1.10/fov.html)
  - the spycam is the same as the picamera v1
- make script start on startup
- stop collecting data on landing, when the pressure data is no longer changing
- Should we truncate the data after a certain point to decrease file size? Like the hundreds or thousands place
  - Looking at the csv file, it seems that the digits repeat themselves, that there are only so many distinct messages

## Assembly instructions

### Parts required

Just made of what I had lying around at the time. Feel free to change the hole sizes to fit your screw through the included Fusion 360 files.

- 10x 5mm M2.5 screws
- 1x 10mm M3 screw
- 1x small rubber band
- Printed parts
  - Spacers were printed out of TPU
  - Rest was printed out of PLA at 215°C and 15% infill

### Things to keep in mind
The screws tap into the plastic, so **do not** over-tighten them.
