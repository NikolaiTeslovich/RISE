# Import packages
import board 
import busio 
import adafruit_lsm303_accel 
import adafruit_lsm303dlh_mag 
from time import sleep

# Connect to the sensors
i2c=busio.I2C(board.SCL, board.SDA)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

while True:
	print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)
	print("Magnetometer (micro-Teslas)): X=%0.3f Y=%0.3f Z=%0.3f"%mag.magnetic)
	print("")
	sleep(0.5)

import time
import board
import busio
import adafruit_bmp3xx

i2c=busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

while True:

        print("Pressure: {:6.1f} Temperature: {:5.2f}".format(bmp.pressure,bmp.temperature))

time.sleep(1)

