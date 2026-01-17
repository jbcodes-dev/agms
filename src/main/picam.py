from picamzero import Camera
from time import sleep



# set directory for storing images
location = "/home/jake/final-year-project/snapshots/"

camera = Camera()

# open camera viewport and stream video feed
camera.start_preview()

# take photo and store in snapshots folder
camera.take_photo(location)

# close viewport
camera.stop_preview()



class PiCam:
    def __init__(self, location):
        pass

    def get_view(self):
        pass

    def close_view(self):
        pass