from datetime import datetime, timedelta
from picamzero import Camera


class RPiCamera:
    def __init__(self, cycle_name):
        self.path = f"/home/jakebrown/final-year-project/snapshots/{cycle_name}/"
        self.camera = Camera()
        self.interval = 30 
        self.last_ss_time = None 
        self.next_ss_time = datetime.now() 
        self.ss_taken = 0

    def take_snapshot(self):
        location = f"{self.path}/{self.ss_taken + 1}.jpg"

        self.camera.still_size = (720, 360)
        self.camera.take_photo(location)

        self.ss_taken += 1

        self.last_ss_time = datetime.now()
        self.next_ss_time = self.last_ss_time + timedelta(seconds=self.interval)

        return location

