from datetime import datetime, timedelta
# from picamzero import Camera
from picamera2.picamera2 import Picamera2, Preview
import time


'''
def cam():
    path = '/home/jakebrown/final-year-project/snapshots/two/'
    file = 'picamera2-test.jpg'
    rpicam = Picamera2()

    config = rpicam.create_preview_configuration()
    rpicam.configure(config)
    rpicam.start()

    time.sleep(2)

    rpicam.capture_file(f'{path}{file}')

    rpicam.stop()

    print(f'image saved to {path} as {file}')
'''


class RPiCamera:
    def __init__(self, cycle_name):
        self.path = f"/home/jakebrown/final-year-project/snapshots/{cycle_name}/"
        self.camera = Picamera2()
        self.config = self.camera.create_preview_configuration()
        self.camera.configure(self.config)
        self.interval = 3600
        self.last_ss_time = None 
        self.next_ss_time = datetime.now() 
        self.ss_taken = 0

    def take_snapshot(self):
        # TODO: add try except statement for checking if directory exists
        location = f"{self.path}{self.ss_taken + 1}.jpg"

        self.camera.start()
        time.sleep(2)
        self.camera.capture_file(location)
        self.camera.stop()

        self.ss_taken += 1

        self.last_ss_time = datetime.now()
        self.next_ss_time = self.last_ss_time + timedelta(seconds=self.interval)

        return location


def main():
    camera = RPiCamera('test')
    camera.take_snapshot()


if __name__ == "__main__":
    main()
