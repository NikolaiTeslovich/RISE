from picamera import PiCamera

# create instance of PiCamera
camera = PiCamera()

# take image
camera.capture("camtest/testimage2.jpg")
