# Screen recording with ffmpeg (start before test, stop after)
import subprocess

def start_recording(name):
    return subprocess.Popen([
        "ffmpeg", "-f", "gdigrab", "-framerate", "10",
        "-i", "desktop", "-y", f"artifacts/videos/{name}.mp4"
    ], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_recording(proc):
    proc.stdin.write(b"q"); proc.stdin.flush(); proc.wait(timeout=10)
```