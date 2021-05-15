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

# Important parameters that can be altered
delay_time = 10
record_time = 60
# How many rows are data are in each temporary file
iters = 200

# Set up I2C and sensors
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

# Make the directory data2 if data1 exists, or data1 if no data directories exist
main_dir = os.listdir('/home/pi/RISE')
names = np.array([0])
for name in main_dir:
    if name.startswith('data'):
        name = np.array([name[4:]]).astype(np.int)
        names = np.append(names, name, axis=0).astype(np.int)
data_dir = f'/home/pi/RISE/data{np.max(names) + 1}'
os.mkdir(data_dir)
print('made directory at ' + data_dir)

# Set up camera stuff
### MAYBE ALSO ITERATE THE CAMERA RECORDINGS ###
### Format the recordings somehow ###
cam = picamera.PiCamera() #intialize camera
cam.resolution = (640, 480)
cam.framerate = 60
cam.start_recording(data_dir + '/' + 'video.h264') #start recording and name video file

# Define the time parameters
start_time = time.time()
i = 0

# Define the function to save a temporary file
def saveTempFile():
    # the formatting (the '{:03}') allows for up to 999 temp files
    file = open(data_dir + '/data' + '{:03}'.format(int(i / iters)) + '.csv', "w")
    np.savetxt(data_dir + '/data' + '{:03}'.format(int(i / iters)) + '.csv', datas, delimiter=",")
    file.close()

# Define one row of the array
datas = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])
# The data collection loop
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
    # Save the data every so often
    if ((i + 1) % iters) == 0:
        #TESTING
        #test_time = time.time()
        saveTempFile()
        # Wipe the array to keep the same save time
        datas = np.array([[]])
        datas = np.array([[(elapsed_time - delay_time), bmp.temperature, bmp.pressure,
                 accel.acceleration[0], accel.acceleration[1], accel.acceleration[2],
                 mag.magnetic[0], mag.magnetic[1], mag.magnetic[2]]])
        #testing
        #print("--- %s seconds to save data ---" % (time.time() - test_time))
# Save the last bit of data after the final loop
saveTempFile()

# Stop the camera recording
cam.stop_recording()

# Make a massive, beautiful csv file at the end with all of the data
all_files = sorted(glob.glob(data_dir + '/' + '*.csv'))
df_from_each_file = (pd.read_csv(f, sep=',', header=None,
                                 names=['time','temperature','pressure',
                                        'acc_x','acc_y','acc_z',
                                        'mag_x','mag_y','mag_z']) for f in all_files)
df_merged = pd.concat(df_from_each_file, axis=0, ignore_index=True)

# a potential fix to a bug
#x = range(0, len(df_merged), 200)

#for n in x:
  #df_merged = df_merged.iloc[n:, :]

# Remove the first row, since the data is off for some reason
df_merged = df_merged.iloc[1: , :]
# Write all of the data to to merged.csv
df_merged.to_csv(data_dir + '/' + 'merged.csv')
# Print done
print('done')
# Exit the program
exit()
