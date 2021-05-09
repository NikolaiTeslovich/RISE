import os
import numpy as np
import board
import busio
import adafruit_bmp3xx
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import time
import picamera

# Setup a directory to save the data in

main_dir = os.listdir('/home/pi/RISE')

names = np.array([0])

for name in main_dir:
    if name.startswith('data'):
        name = np.array([name[-1]]).astype(np.int)
        names = np.append(names, name, axis=0).astype(np.int)

data_dir = f'/home/pi/RISE/data{np.max(names) + 1}'

os.mkdir(data_dir)

print('made directory at ' + data_dir)

# Set up I2C and sensors

i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

# Define the time parameters

start_time = time.time()
delay_time = 1
record_time = 60

# iterating parameters

i = 0
iters = 100

elapsed_time = time.time() - start_time

# Define the array with all of the data

datas = np.array([[(elapsed_time - delay_time), bmp.temperature, bmp.pressure,
                 accel.acceleration[0], accel.acceleration[1], accel.acceleration[2],
                 mag.magnetic[0], mag.magnetic[1], mag.magnetic[2]]])

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
        file = open(data_dir + '/' + f'data{int(i / iters)}.csv', "w")
        np.savetxt(data_dir + '/' + f'data{int(i / iters)}.csv', datas, delimiter=",")
        file.close()
        #wipe the array to keep the same save time
        datas = np.array([[]])
        datas = np.array([[(elapsed_time - delay_time), bmp.temperature, bmp.pressure,
                 accel.acceleration[0], accel.acceleration[1], accel.acceleration[2],
                 mag.magnetic[0], mag.magnetic[1], mag.magnetic[2]]])
        #testing
        print("--- %s seconds to save data ---" % (time.time() - test_time))

#save the last bit of data after the final loop
file = open(data_dir + '/' + f'data{int((i / iters) + 1)}.csv', "w")
np.savetxt(data_dir + '/' + f'data{int((i / iters) + 1)}.csv', datas, delimiter=",")
file.close()


print(done sir)
