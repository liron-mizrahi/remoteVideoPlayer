import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, VIDEO_FOLDER, video_player

client = TestClient(app)

def setup_module(module):
    # Ensure test video files exist
    os.makedirs(VIDEO_FOLDER, exist_ok=True)
    with open(os.path.join(VIDEO_FOLDER, 'test.mp4'), 'w') as f:
        f.write('fake')

def teardown_module(module):
    # Clean up test video files
    try:
        os.remove(os.path.join(VIDEO_FOLDER, 'test.mp4'))
    except Exception:
        pass

def test_list_videos():
    response = client.get('/videos')
    assert response.status_code == 200
    assert 'test.mp4' in response.json()

def test_play_video(monkeypatch):
    def fake_play(filename):
        video_player.is_playing = True
        video_player.current_video = filename
    monkeypatch.setattr(video_player, 'play', fake_play)
    response = client.post('/play', json={'filename': 'test.mp4'})
    assert response.status_code == 200
    assert response.json()['status'] == 'playing'

def test_pause_video(monkeypatch):
    def fake_pause():
        video_player.is_paused = True
    monkeypatch.setattr(video_player, 'pause', fake_pause)
    response = client.post('/pause')
    assert response.status_code == 200
    assert response.json()['status'] == 'paused'

def test_stop_video(monkeypatch):
    def fake_stop():
        video_player.is_playing = False
    monkeypatch.setattr(video_player, 'stop', fake_stop)
    response = client.post('/stop')
    assert response.status_code == 200
    assert response.json()['status'] == 'stopped'
