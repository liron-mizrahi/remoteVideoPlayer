# Harel GUI2 Video Playback System

## Overview
This application is a video playback system designed to allow remote control of video playback on a backend server. It consists of:
- **Backend:** Python-based, using FastAPI for the web server and VLC for video playback.
- **Frontend:** Next.js application that communicates with the backend via API requests.

## Features
- **Video List:** The frontend displays a list of video files available in a specific folder on the backend server.
- **Remote Playback Control:** Users can select a video from the list and control playback (play, pause/resume, stop, mute/unmute, adjust volume) from the frontend.
- **Fullscreen Playback:** When a video is played, it is displayed in fullscreen mode on the backend server's monitor.
- **Live Controls:** The frontend provides play, pause/resume, stop, mute/unmute, and volume controls that send commands to the backend, allowing real-time control of the video.
- **Switch Videos:** Users can switch to a different video at any time during playback.

## Architecture
- **Backend:**
  - Built with FastAPI for handling API requests from the frontend.
  - Uses VLC media player with its RC (remote control) interface for video playback.
  - Exposes endpoints for listing available videos, playing, pausing/resuming, stopping, muting/unmuting, and adjusting volume.
- **Frontend:**
  - Built with Next.js and React.
  - Sends API requests to the backend to control video playback.
  - Displays the list of available videos and provides playback controls.

## Backend API Endpoints
- `GET /videos`: Lists available video files.
- `POST /play`: Starts playback of a selected video.
- `POST /pause`: Pauses the video.
- `POST /unpause`: Resumes the video.
- `POST /stop`: Stops the video.
- `POST /volume`: Adjusts the volume (0-256 scale).
- `POST /mute`: Mutes the audio.
- `POST /unmute`: Unmutes the audio.

## Frontend Features
- **Video List:** Scrollable list of available videos.
- **Playback Controls:** Buttons for play, pause/resume, stop, mute/unmute, and a slider for volume control.
- **Responsive Design:** Optimized for desktop and mobile devices.
- **Error Handling:** Displays warnings if the backend is unreachable or no videos are available.

## Design Considerations
- **Backend:**
  - VLC was chosen for its robust video playback capabilities and support for remote control via the RC interface.
  - The backend uses a simple RESTful interface for ease of integration with the frontend.
  - Mute/unmute functionality was implemented using volume control for reliability on macOS.
- **Frontend:**
  - Next.js was chosen for its ease of development and server-side rendering capabilities.
  - The UI is designed to be intuitive and responsive, ensuring a seamless user experience.

## Usage
1. **Start the Backend Server:**
   - Run the FastAPI server using `start.sh`.
   - Ensure the `videos/` folder contains the video files you want to make available.
2. **Access the Frontend:**
   - Open the Next.js frontend in your browser.
   - Select a video and use the controls to play, pause/resume, stop, mute/unmute, or adjust volume.

## Requirements
- Python 3.x
- FastAPI
- VLC media player
- Node.js (for the frontend)
- Next.js

## Folder Structure
- `main.py` - Entry point for the backend server.
- `videos/` - Folder containing video files to be listed and played.
- `frontend/` - Contains the Next.js frontend application.
- `README.md` - This file.
- `start.sh` - Script to start both backend and frontend.

## Notes
- The backend server must have a display connected for fullscreen playback.
- VLC must be installed and accessible on the backend server.
- The frontend is included in this repository and can be started using `npm run dev`.

---

For more details, see the code in `main.py` and the `frontend/` directory.



