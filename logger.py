from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    message = f"[LOG]{timestamp}{message}"

    with open("log.txt", "a") as file:
        file.write(f"{message}\n")

    print(message)
