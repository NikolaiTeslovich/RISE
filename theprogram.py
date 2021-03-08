Flight time is estimated to be three minutes

import pandas
import board
import busio
import adafruit_bmp3xx
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import time #time package (if you wa©nt to use the sleep command and/or keep track of time)
import picamera #running the spycamera while gathering datas

##### set up I2C and sensors #####
i2c = busio.I2C(board.SCL,board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

##### let's say we want to make a list of all sensor measurements and alo keep track of time... #####
#set up a DataFrame with columns time, for temp, pressure, 3 columns for acceleraton and 3 for magnetometer
df = pandas.DataFrame(columns=['time','temperature','pressure',
								'acc_x','acc_y','acc_z',
								'mag_x','mag_y','mag_z'])

# CHECK OTHER CAMERA FUNCTIONS https://picamera.readthedocs.io/en/release-1.12/fov.html

## Compare pressure sensor data to make it work

start_time = time.time() #reference for t = 0
camera = picamera.PiCamera() #intiialize camera
camera.resolution = (1296, 972) #set camera resolution, this one utilized the whole sensor while keeping a decent framerate
camera.framerate = 30
camera.start_recording('testvid.h264') #start recording and name video file

while True:

	for i in range(100): #repeat measurements and data append 10 times (perahps increase to 100 or 1000)
		elapsed_time = time.time() - start_time # current time in seconds since start_time
		df = df.append({'time':elapsed_time, #add in current time
					'temperature':bmp.temperature,
					'pressure':bmp.pressure,
					'accx':accel.acceleration[0],
					'accy':accel.acceleration[1],
					'accz':accel.acceleration[2],
					'magx':mag.magnetic[0],
					'magy':mag.magnetic[1],
					'magz':mag.magnetic[2]}, ignore_index=True)

	df.to_csv('data.csv') #to save data as CSV file



camera.stop_recording()
total_elapsed = time.time() - start_time
print(total_elapsed)
