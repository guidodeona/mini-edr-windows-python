import os
import datetime

LOG_FILE = "logs/actividad.log"

def log_event(msg):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{hora}] {msg}\n")
