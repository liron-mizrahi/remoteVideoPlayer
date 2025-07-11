import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import threading
import configparser


# VLC imports
import subprocess
import signal
import sys

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load VIDEO_FOLDER from env.ini
config = configparser.ConfigParser()
config.read("env.ini")
VIDEO_FOLDER = config.get("settings", "VIDEO_FOLDER", fallback="videos")
VLC_PATH = config.get("settings", "VLC_PATH", fallback="/Applications/VLC.app/Contents/MacOS/VLC")


class VideoControl(BaseModel):
    filename: str



# --- NEW VideoPlayer using main-thread VLC event loop ---
import queue

import socket

class VideoPlayer:
    def __init__(self):
        self.process = None
        self.current_video = None
        self.is_playing = False
        self.is_paused = False
        self.rc_socket = None

    def _connect_rc(self):
        # Connect to VLC RC interface
        if self.rc_socket is None:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", 4212))
                self.rc_socket = s
                # Read welcome message
                self.rc_socket.recv(1024)
            except Exception as e:
                print(f"RC connect error: {e}")
                self.rc_socket = None

    def _send_rc(self, cmd):
        self._connect_rc()
        if self.rc_socket:
            try:
                self.rc_socket.sendall((cmd + "\n").encode())
                return self.rc_socket.recv(1024).decode()
            except Exception as e:
                print(f"RC send error: {e}")
                self.rc_socket = None
        return None

    def play(self, filename):
        self.stop()
        abs_path = os.path.abspath(filename)
        print(f"Playing: {abs_path}")
        # Launch VLC with RC interface
        self.process = subprocess.Popen([
            VLC_PATH,
            "--fullscreen",
            "--no-video-title-show",
            "--extraintf=rc",
            "--rc-host=127.0.0.1:4212",
            abs_path
        ])
        self.current_video = abs_path
        self.is_playing = True
        self.is_paused = False
        self.rc_socket = None

    def pause(self):
        if self.process and self.process.poll() is None:
            self._send_rc("pause")
            self.is_paused = True

    def unpause(self):
        if self.process and self.process.poll() is None:
            self._send_rc("pause")
            self.is_paused = False

    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                self._send_rc("stop")
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception as e:
                print(f"Stop error: {e}")
            self.process = None
            self.is_playing = False
            self.is_paused = False
            self.current_video = None
        if self.rc_socket:
            try:
                self.rc_socket.close()
            except Exception:
                pass
            self.rc_socket = None

    def set_volume(self, vol):
        # vol: 0-256 (VLC RC scale)
        if self.process and self.process.poll() is None:
            self._send_rc(f"volume {int(vol)}")
        self._last_volume = int(vol) if int(vol) > 0 else getattr(self, '_last_volume', 256)

    def set_mute(self, mute):
        if self.process and self.process.poll() is None:
            # Workaround for macOS: set volume 0 for mute, restore previous for unmute
            resp = self._send_rc("status")
            current_vol = 256
            if resp:
                for line in resp.splitlines():
                    if "volume:" in line:
                        try:
                            current_vol = int(line.split("volume:")[1].split("/")[0].strip())
                        except Exception:
                            pass
            if mute:
                self._last_volume = current_vol if current_vol > 0 else getattr(self, '_last_volume', 256)
                self.set_volume(0)
            else:
                restore_vol = getattr(self, '_last_volume', 256)
                self.set_volume(restore_vol)
# --- END NEW VideoPlayer ---


# --- Volume and Mute Endpoints ---
from fastapi import Query

@app.post("/volume")
def set_volume(level: int = Query(..., ge=0, le=256)):
    video_player.set_volume(level)
    return JSONResponse(content={"status": "volume", "level": level})

@app.post("/mute")
def set_mute():
    video_player.set_mute(True)
    return JSONResponse(content={"status": "muted"})

@app.post("/unmute")
def set_unmute():
    video_player.set_mute(False)
    return JSONResponse(content={"status": "unmuted"})

# --- END NEW VideoPlayer ---


video_player = VideoPlayer()


@app.get("/videos", response_model=List[str])
def list_videos():
    files = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))]
    return files

@app.post("/play")
def play_video(control: VideoControl):
    filepath = os.path.join(VIDEO_FOLDER, control.filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    print(filepath)
    video_player.play(filepath)
    return JSONResponse(content={"status": "playing", "file": control.filename})

@app.post("/pause")
def pause_video():
    video_player.pause()
    return JSONResponse(content={"status": "paused"})

@app.post("/unpause")
def unpause_video():
    video_player.unpause()
    return JSONResponse(content={"status": "unpaused"})

@app.post("/stop")
def stop_video():
    video_player.stop()
    return JSONResponse(content={"status": "stopped"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
