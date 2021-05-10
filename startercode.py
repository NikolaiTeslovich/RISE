import pandas
import board
import busio
import adafruit_bmp3xx
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
##### let's add in some extra functionality #####
import time #time package (if you want to use the sleep command and/or keep track of time)
import picamera #running the spycamera while gathering datas

##### set up I2C and sensors #####
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

##### let's say we want to make a list of all sensor measurements and alo keep track of time... #####
df = pandas.DataFrame(columns=['time','temperature','pressure',
			       'acc_x','acc_y','acc_z',
			       'mag_x','mag_y','mag_z'])
#set up a DataFrame with columns time, for temp, pressure, 3 columns for acceleraton and 3 for magnetometer

# Set up camera stuff.
cam = picamera.PiCamera() #intiialize camera
cam.resolution = (640,800) #set camera resolution
cam.start_recording('test_video.h264') #start recording and name video file

# Define start time, delay, and total elapsed time.
start_time = time.time()
delay_time = 100
record_time = 500

# print('Start')

elapsed_time = time.time() - start_time
while elapsed_time < delay_time + record_time:
    # Update elapsed time.
    elapsed_time = time.time() - start_time
    # Skip everything else if we're still in delay period.
    if elapsed_time < delay_time:
        continue
    # Otherwise, append data to dataframe.
    df = df.append({'time':elapsed_time,
                    'temperature':bmp.temperature,
	  	    		'pressure':bmp.pressure,
		    		'acc_x':accel.acceleration[0],
	            	'acc_y':accel.acceleration[1],
		    		'acc_z':accel.acceleration[2],
		    		'mag_x':mag.magnetic[0],
	            	'mag_y':mag.magnetic[1],
		    		'mag_z':mag.magnetic[2]},
		    		ignore_index=True)

# Stop camera recording.
cam.stop_recording()

# Save data.
df.to_csv('test_data.csv')

# Specific to testing this code. Let's you know it's done.
total_elapsed = time.time() - start_time
print(total_elapsed)
