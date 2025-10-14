import subprocess
import time
import sys
import os

script_path = os.path.join(os.path.dirname(__file__), "widget.py")

while True:
    # Start the widget silently (no console window)
    process = subprocess.Popen(
        [sys.executable, script_path],
        creationflags=subprocess.CREATE_NO_WINDOW  # <-- makes it silent
    )

    # Wait for the widget to exit
    process.wait()

    # If it closes or is killed, restart after short delay
    time.sleep(2)
