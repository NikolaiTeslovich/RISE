import os
import glob
import numpy as np
import board
import busio
import adafruit_bmp3xx
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import time
import picamera
import pandas as pd

# Setup a directory to save the data in

main_dir = os.listdir('/home/pi/RISE')

names = np.array([0])

for name in main_dir:
    if name.startswith('data'):
        name = np.array([name[4:]]).astype(np.int)
        names = np.append(names, name, axis=0).astype(np.int)

data_dir = f'/home/pi/RISE/data{np.max(names) + 1}'

os.mkdir(data_dir)

print('made directory at ' + data_dir)

# Set up I2C and sensors

i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

# Set up camera stuff
### MAYBE ALSO ITERATE THE CAMERA RECORDINGS ###
### Format the recordings somehow ###
# cam = picamera.PiCamera() #intialize camera
# cam.resolution = (640, 480)
# camera.framerate = 90
# cam.start_recording(data_dir + '/' + 'video.h264') #start recording and name video file

# Define the time parameters

start_time = time.time()
delay_time = 10
record_time = 300

# iterating parameters

i = 0

## find a good interval for this value
iters = 200

elapsed_time = time.time() - start_time

# Define the array with all of the data

datas = np.array([[(elapsed_time - delay_time), bmp.temperature, bmp.pressure,
                 accel.acceleration[0], accel.acceleration[1], accel.acceleration[2],
                 mag.magnetic[0], mag.magnetic[1], mag.magnetic[2]]])

# Define the function to save a temporary file
def saveTempFile():
    # the formatting (the '{:03}') allows for up to 999 temp files
    file = open(data_dir + '/data' + '{:03}'.format(int(i / iters)) + '.csv', "w")
    np.savetxt(data_dir + '/data' + '{:03}'.format(int(i / iters)) + '.csv', datas, delimiter=",")
    file.close()

while time.time() - start_time < delay_time + record_time:
    # Update elapsed time with every run
    elapsed_time = time.time() - start_time
    # Skip everything else if we're still in the delay period
    if elapsed_time < delay_time:
        continue
    # Append data to the array
    data = np.array([[(elapsed_time - delay_time), bmp.temperature, bmp.pressure,
                 accel.acceleration[0], accel.acceleration[1], accel.acceleration[2],
                 mag.magnetic[0], mag.magnetic[1], mag.magnetic[2]]])
    datas = np.append(datas, data, axis=0)

    i += 1

    #save the data every so often
    if ((i + 1) % iters) == 0:
        #TESTING
        test_time = time.time()
        saveTempFile()
        #wipe the array to keep the same save time
        datas = np.array([[]])
        datas = np.array([[(elapsed_time - delay_time), bmp.temperature, bmp.pressure,
                 accel.acceleration[0], accel.acceleration[1], accel.acceleration[2],
                 mag.magnetic[0], mag.magnetic[1], mag.magnetic[2]]])
        #testing
        print("--- %s seconds to save data ---" % (time.time() - test_time))

#save the last bit of data after the final loop
saveTempFile()

# Stop the camera recording
#cam.stop_recording()

# make a massive, beautiful csv file at the end with all of the data
all_files = sorted(glob.glob(data_dir + '/' + '*.csv'))
df_from_each_file = (pd.read_csv(f, sep=',', header=None,
                                 names=['time','temperature','pressure',
                                        'acc_x','acc_y','acc_z',
                                        'mag_x','mag_y','mag_z']) for f in all_files)
df_merged = pd.concat(df_from_each_file, axis=0, ignore_index=True)
df_merged.to_csv(data_dir + '/' + 'merged.csv')

print('done')
