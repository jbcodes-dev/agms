from picamzero import Camera 
from datetime import datetime, timedelta


class PiCam:
    def __init__(self, path: str):
        """
        Initialise PiCam with path to image location.
        
        path: string for path to image storage.
        """

        self._path = path

        self._cam = Camera()

        # seconds between snapshots
        self._interval = 3600

        self._last_snapshot_time = None
        self._next_snapshot_time = None
        self._snapshots_taken = 0

    def take_snapshot(self) -> str:
        """
        Take photo of current view, set new snapshot time.

        location: return string for photo location to store in database.
        """

        # set location of new image
        location = f"{self._path}/{self._snapshots_taken + 1}.jpg"

        # set photo resolution and take photo
        self._cam.still_size = (720, 360)
        self._cam.take_photo(location)
        
        # increment snapshot count
        self._snapshots_taken += 1

        # set new snapshot time
        self._last_snapshot_time = datetime.now()
        self._next_snapshot_time = self._last_snapshot_time + timedelta(seconds=self._interval)
        
        # return path to photo
        return location 
