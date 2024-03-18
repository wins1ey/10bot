from datetime import datetime

class Logger:

    def __init__(self, filename = "log.txt"):
        self.filename = filename

    def log(self, message):

        # Get timestamp of log entry.
        timestamp = datetime.now().strftime("[%H:%M:%S]")

        # Write to console.
        print("[LOG] " + message)

        # Write to logfile.
        with open(self.filename, "a") as file:
            file.write("[LOG]" + timestamp + message + "\n")