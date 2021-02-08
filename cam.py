from picamera import PiCamera
from time import sleep

# create instance of PiCamera
camera = PiCamera()

# take image
# camera.capture("camtest/testimage2.jpg")

camera.start_recording("camtest/vid1.h264")
sleep(10)
camera.stop_recording()
