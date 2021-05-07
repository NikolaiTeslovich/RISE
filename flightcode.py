import os
import pandas
import board
import busio
import adafruit_bmp3xx
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import time
import picamera

#Delete the csvs if they already exist#
for file_name in os.listdir('/home/pi/RISE/data'):
    if file_name.endswith('.csv'):
        os.remove(f'/home/pi/RISE/data/{file_name}')

##### set up I2C and sensors #####
i2c = busio.I2C(board.SCL,board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

#set up a DataFrame with columns time, for temp, pressure, 3 columns for acceleraton and 3 for magnetometer
df = pandas.DataFrame(columns=['time','temperature','pressure',
                               'acc_x','acc_y','acc_z',
                               'mag_x','mag_y','mag_z'])

# Set up camera stuff.
### MAYBE ALSO ITERATE THE CAMERA RECORDINGS ###
# cam = picamera.PiCamera() #intiialize camera
# cam.resolution = (640, 480) #Figure out best cam resolution, linked in GitHub
# camera.framerate = 90
# cam.start_recording('video.h264') #start recording and name video file

# Define start time, delay, and total elapsed time
start_time = time.time()
delay_time = 5
record_time = 20

# iteration
i = 0
itersperfile = 10

# FOR TESTING
print('Start')

elapsed_time = time.time() - start_time

while time.time() - start_time < delay_time + record_time:
    # Update elapsed time
    elapsed_time = time.time() - start_time
    # Skip everything else if we're still in delay period
    if elapsed_time < delay_time:
        continue
    # Otherwise, append data to dataframe
    df = df.append({'time':(elapsed_time - delay_time),
                    'temperature':bmp.temperature,
		    'pressure':bmp.pressure,
		    'acc_x':accel.acceleration[0],
	            'acc_y':accel.acceleration[1],
		    'acc_z':accel.acceleration[2],
		    'mag_x':mag.magnetic[0],
	            'mag_y':mag.magnetic[1],
		    'mag_z':mag.magnetic[2]},
		    ignore_index=True)
    
    # start the counter
    i += 1
    
    if (i % itersperfile) == 0:
        df.to_csv(f'/home/pi/RISE/data/data_temporary_{int(i / itersperfile)}.csv', index = False)
        # for testing purposes
        print('data saved!')

# save all the data in one file, if the program ran successfully
df.to_csv('/home/pi/RISE/data/data.csv', index = False)

# if the program managed to run successfully, remove the temporary files
for file_name in os.listdir('/home/pi/RISE/data'):
    if file_name.startswith('data_temporary') and file_name.endswith('.csv'):
        os.remove(f'/home/pi/RISE/data/{file_name}')

# Stop camera recording
#cam.stop_recording()

# Save data
# df.to_csv(f'data{i / 1000}.csv', index = False)

# FOR TESTING
print('Finished')
print(elapsed_time)
