from datetime import datetime

def log(message: str, level="INFO"):
    """
    Prints a formatted log message to the console.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}] {message}")
