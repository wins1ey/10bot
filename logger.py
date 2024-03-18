from datetime import datetime

def log(message):

    # Get timestamp of log entry.
    timestamp = datetime.now().strftime("[%H:%M:%S]")

    # Write to console.
    print("[LOG] " + message)

    # Write to logfile.
    with open("log.txt", "a") as file:
         file.write("[LOG]" + timestamp + message + "\n")