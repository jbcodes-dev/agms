"""
Author: Jake Brown
ID: 001239595
Purpose: logger class for generating log files for debugging and tracking program execution.
"""

from datetime import datetime


class Logger:
    def __init__(self, filename):
        """ Initialise logger with filename. """
        self.filename = filename
        self.new_session()
    
    def new_session(self):
        """ Split old session from new session in log file. """
        with open(self.filename, 'a') as file:
            file.append("\n########## {datetime.now()} ##########\n")


    def log(self, type, msg):
        """ Write to a log file. """
        
        with open(self.filename, 'a') as file:
            if type == "debug":
                prefix = "[DEBUG]"
            elif type == "test":
                prefix = "[TEST]"
            else:
                type == f"[{type}]"

            file.append(f"{prefix} ({datetime.now()}) {msg}")
