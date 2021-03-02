import pandas
import board
import busio
import adafruit_bmp3xx
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import time #time package (if you want to use the sleep command and/or keep track of time)
import picamera #running the spycamera while gathering datas

##### set up I2C and sensors #####
i2c = busio.I2C(board.SCL,board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

##### let's say we want to make a list of all sensor measurements and alo keep track of time... #####
df = pandas.DataFrame(columns=['time','temperature','pressure',
								'acc_x','acc_y','acc_z',
								'mag_x','mag_y','mag_z'])
#set up a DataFrame with columns time, for temp, pressure, 3 columns for acceleraton and 3 for magnetometer

# CHECK OTHER CAMERA FUNCTIONS

start_time = time.time() #reference for t=0
cam = picamera.PiCamera() #intiialize camera
cam.resolution = (640,800) #set camera resolution
cam.start_recording('testvid.h264') #start recording and name video file

for i in range(10): #repeat measurements and data append 10 times (perahps increase to 100 or 1000)
	elapsed_time = time.time() - start_time # current time in seconds since start_time
	df = df.append({'time':elapsed_time, #add in current time
					'temperature':bmp.temperature,
					'pressure':bmp.pressure,
					'accx':accel.acceleration[0],
					'accy':accel.acceleration[1],
					'accz':accel.acceleration[2],
					'magx':mag.magnetic[0],
					'magy':mag.magnetic[1],
					'magz':mag.magnetic[2]},ignore_index=True)
	time.sleep(1) #optional: specify rate of data collection

cam.stop_recording()
df.to_csv('data.csv') #to save data as CSV file
total_elapsed = time.time() - start_time
print(total_elapsed)
