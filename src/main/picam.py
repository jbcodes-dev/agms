from picamzero import Camera 
from datetime import datetime, timedelta


class PiCam:
    def __init__(self, path):
        self._path = path
        self._cam = Camera()
        self._last_snapshot_time = None
        self._interval = 3600
        self._next_snapshot_time = None
        self._snapshots_taken = 0

    def take_snapshot(self):
        location = f"{self._path}/{self._snapshots_taken + 1}.jpg"

        # add current time to photo
        # self._cam.annotate(str(datetime.now()))

        # set photo resolution
        # self._cam.still_size(720, 360)
        self._cam.take_photo(location)
        
        self._snapshots_taken += 1
        self._last_snapshot_time = datetime.now()
        self._next_snapshot_time = self._last_snapshot_time + timedelta(seconds=self._interval)
        
        return location 
