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

### 3D Printing instructions
- Spacers were printed out of TPU
- Everything else was printed out of PLA at 215°C and 15% infill

### Parts required
Just made of what I had lying around at the time. Feel free to change the hole sizes to fit your screw sizes through the included Fusion 360 files.

- [GNB 450mah 1s LiHV](https://www.amazon.com/PowerWhoop-Connector-Tinyhawk-Brushless-Inductrix/dp/B078Y3Y4ZZ/ref=sr_1_9?dchild=1&keywords=450mah+1s&qid=1617315333&sr=8-9), it's what I use in my super small FPV drones
- 10x 5mm M2.5 screws
- 1x 10mm M3 screw
- 1x small rubber band
- Printed parts (obviously)

### Things to keep in mind
The screws tap into the plastic, so **do not** over-tighten them. Other than that, assembly should be pretty self-explanatory.
