from .logger import log_event

def print_alert(msg, level="info"):
    colors = {
        "info": "\033[94m",
        "warning": "\033[93m",
        "danger": "\033[91m",
        "success": "\033[92m"
    }
    print(colors.get(level, "\033[0m") + msg + "\033[0m")
    log_event(msg)
