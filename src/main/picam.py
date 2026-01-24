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
        filename = f"{self._snapshots_taken + 1}.jpg"

        self._cam.take_photo(filename)
        
        self._snapshots_taken += 1
        self._last_snapshot_time = datetime.now()
        self._next_snapshot_time = self._last_snapshot_time + timedelta(seconds=self._interval)
        
        return filename