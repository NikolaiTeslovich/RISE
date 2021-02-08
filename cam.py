from picamera import PiCamera

# create instance of PiCamera
camera = PiCamera()

# take image
camera.capture("~/RISE/testimage2.jpg")
