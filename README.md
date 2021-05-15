<h1 align="center">
  The Rocket Lab Initiative — RISE
</h1>

<p align="center">
  <img src="/resources/RISE.png" width="150" height="150">
</p>

<p align="center">
  <a href="https://github.com/NikolaiTeslovich/RISE/blob/main/LICENSE">
    <img alt="MIT license" src="https://img.shields.io/github/license/NikolaiTeslovich/RISE">
  </a>
</p>

<p align="center">
  A payload that collects data and video throughout the flight of a model rocket.
</p>

# To do

- find appropriate camera resolution and framerate, [here's a helpful article](https://picamera.readthedocs.io/en/release-1.10/fov.html)
  - the spycam is the same as the picamera v1
  - does this affect the rate of data collection?
- Error encountered involving duplicate values with the data collections

# Breakdown of the code

1. First it imports the packages, sets up the sensors over I2C, and starts recording video.
2. Creates a new directory to put the data and video into, to prevent overwriting any data.
    - If no data directories exist, create the `data1` directory.
    - If the `data1` directory already exists, create the `data2` directory, etc.
3. Waits until the `delay_time` is over to collect data from the sensors as fast as possible using a [NumPy](https://numpy.org/) array over the `record_time` interval.
    - This comes out to about 40 measurements/sec compared to ~10 measurements/sec if I had used [pandas](https://pandas.pydata.org/) dataframes.
4. Every so many rows defined by the `iters` variable, dump the data into a csv and wipe the array.
    - This is done for bullet-proofness, so that if the payload breaks, data up to that point is saved.
    - The save time is only about ~0.1s.
5. When the `record_time` is over, the last of data is saved into a csv, and the camera stops recording.
6. All of the temporary csv files are merged into one `merged.csv` through the use of a dataframe (I found pandas the easiest way to do this).

**Note**. If your data gets corrupted for some reason, for example due to a random power out, run this command in the repo directory:

```
find .git/objects/ -size 0 -exec rm -f {} \; && git fetch origin
```

# Payload instructions

## Disclaimer

This is by far not the easiest thing to assemble, so if you are not confident in you tweezer usage skills when ribbon cables are involved, I recommend cutting out a hole in the rocket and mounting the camera facing sideways rather than down.

## Making the Pi headless

*And I didn't just chop off its head.*

Headless means that no connections to the Pi other than power and the network are needed to use it, essentially like a server.

### Install the Operating System (Pi OS Lite)

Raspberry Pi Imager is an app to make installing the operating system on your SD card a breeze.

Download it below:

https://www.raspberrypi.org/software/

Then, plug in the SD card and flash it with **Raspberry Pi OS Lite**.

### Making the Pi work headlessly

Remove, then plug back in the SD card.

In a terminal window, run:

```
touch /Volumes/boot/ssh
```

This will make a file on the SD card called `ssh`, which will enable ssh on the Pi.

Next, let's add some wifi information by creating another file on the SD card:

```
touch /Volumes/boot/wpa_supplicant.conf
```

Open the file with a text editing utility like TextEdit or nano, and paste in the following, substituting `NETWORK-NAME` with your wifi name and `NETWORK-PASSWORD` with the wifi password:

```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
}
```

Save the changes to the file, and eject the SD from your computer. The Pi is ready for its first boot.

###  Connecting to the Pi over ssh

After waiting for a couple minutes (the first boot takes quite a bit of time), connect to the Pi with this command, substituting the `ipaddress` with the ip of the Pi, which you can get through your router:

```
ssh pi@ipaddress
```

The password for the pi user is `raspberry`.

Then, update the Pi:

```
sudo apt update && sudo apt upgrade -y
```

To exit the ssh session just type `exit`.

### Making the code run on startup

Create a cron job, and selected the `[1]` option to edit it in nano:

```
crontab -e
```

At the very bottom, add the following to run the script on startup:

```
@reboot python3 /home/pi/RISE/flightcode.py &
```

*Important*: be sure to leave a line below the text, or else it might not work.

Exit out of nano by pressing ctrl-X followed by Y to save the changes.

Now, with a reboot the script should work.

### Transferring the data from the Pi to your computer with scp

The -r option is used to copy a directory, while the -p option is used to preserve file modification and access times.

Here's the general syntax:

```
scp -r -p remote_username@ip:/data_directory /local/directory
```

So for my use case, it would look like this (ip address omitted for obvious reasons):

```
scp -r -p pi@192.xxx.xxx.xxx:/home/pi/RISE/data1 ~/Downloads
```

The secure copy command connects to the pi and copies the directory at `/home/pi/RISE/data1/` to my computer's user Download directory `~/Downloads`.

## Sensor payload & camera assembly

| ![SensorPayload Side 1](/resources/payload1.jpg) | ![SensorPayload Side 2](/resources/payload2.jpg) |
| :---: | :---: |
|  Camera, sensor & voltage regulator  |  Raspberry Pi Zero W  |

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

![ShortedPowerBoost](/resources/shortedpowerboost.jpeg)

# Some beautiful photographs

| ![Rocket](/resources/rocket.jpeg) | ![Payload inside rocket](/resources/payloadinrocket.jpeg) |
| :---: | :---: |
|  The rocket  |  Payload in the rocket  |

Last but not least, here is the external camera:

![Camera mounted externally](/resources/camera.jpeg)
