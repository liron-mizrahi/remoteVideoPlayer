import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [videos, setVideos] = useState([]);
  const [selected, setSelected] = useState(null);
  const [status, setStatus] = useState('');
  const [volume, setVolume] = useState(1);
  const [muted, setMuted] = useState(false);
  const [activeBtn, setActiveBtn] = useState('');
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    axios.get('/api/videos')
      .then(res => setVideos(res.data))
      .catch(() => setVideos([]));
  }, []);

  const handlePlay = () => {
    if (selected) {
      setActiveBtn('play');
      axios.post('/api/play', { filename: selected }).then(res => {
        setStatus(res.data.status);
        setPaused(false);
      });
    }
  };
  const handlePauseResume = () => {
    if (!paused) {
      setActiveBtn('pause');
      axios.post('/api/pause').then(res => {
        setStatus(res.data.status);
        setPaused(true);
      });
    } else {
      setActiveBtn('pause');
      axios.post('/api/unpause').then(res => {
        setStatus(res.data.status);
        setPaused(false);
      });
    }
  };
  const handleStop = () => {
    setActiveBtn('stop');
    axios.post('/api/stop').then(res => {
      setStatus(res.data.status);
      setPaused(false);
    });
  };
  const handleVolume = (e) => {
    const v = Number(e.target.value);
    setVolume(v);
    // VLC RC volume is 0-256
    axios.post('/api/volume', { level: Math.round(v * 256) });
    if (muted && v > 0) setMuted(false);
  };
  const handleMute = () => {
    if (!muted) {
      axios.post('/api/mute').then(() => setMuted(true));
    } else {
      axios.post('/api/unmute').then(() => setMuted(false));
    }
  };

  return (
    <div className="container">
      <h1>Video Player Remote</h1>
      <div className="video-list">
        <h2>Available Videos</h2>
        {videos.length === 0 ? (
          <div className="warning">No connection to backend or no videos found.</div>
        ) : (
          <ul>
            {videos.map(v => (
              <li key={v} className={selected === v ? 'selected' : ''} onClick={() => setSelected(v)}>{v}</li>
            ))}
          </ul>
        )}
      </div>
      <div className="controls">
        <button
          className={activeBtn === 'play' ? 'toggle pressed' : 'toggle'}
          onClick={handlePlay}
          disabled={!selected}
        >Play</button>
        <button
          className={activeBtn === 'pause' ? 'toggle pressed' : 'toggle'}
          onClick={handlePauseResume}
        >{paused ? 'Resume' : 'Pause'}</button>
        <button
          className={activeBtn === 'stop' ? 'toggle pressed' : 'toggle'}
          onClick={handleStop}
        >Stop</button>
        <button
          className={muted ? 'toggle pressed' : 'toggle'}
          onClick={handleMute}
        >{muted ? 'Unmute' : 'Mute'}</button>
        <input type="range" min="0" max="1" step="0.01" value={muted ? 0 : volume} onChange={handleVolume} disabled={muted} />
      </div>
      <div className="status">Status: {status}</div>
      <style jsx>{`
        .container {
          max-width: 400px;
          margin: auto;
          padding: 1rem;
          font-family: sans-serif;
        }
        .video-list {
          max-height: 200px;
          overflow-y: auto;
          background: #f9f9f9;
          border-radius: 8px;
          margin-bottom: 1rem;
        }
        .warning {
          color: #b71c1c;
          background: #ffeaea;
          padding: 1rem;
          border-radius: 6px;
          text-align: center;
        }
        ul {
          list-style: none;
          padding: 0;
          margin: 0;
        }
        li {
          padding: 0.5rem 1rem;
          cursor: pointer;
        }
        li.selected {
          background: #0070f3;
          color: white;
        }
        .controls {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          justify-content: center;
          margin-bottom: 1rem;
        }
        .toggle {
          padding: 0.5rem 1rem;
          border: none;
          border-radius: 4px;
          background: #0070f3;
          color: white;
          font-size: 1rem;
          transition: background 0.1s, box-shadow 0.1s;
          box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .toggle.pressed {
          background: #005bb5;
          box-shadow: 0 1px 2px rgba(0,0,0,0.10) inset;
        }
        button:disabled {
          background: #ccc;
        }
        input[type='range'] {
          width: 100px;
        }
        .status {
          text-align: center;
          margin-top: 1rem;
        }
        @media (max-width: 600px) {
          .container {
            max-width: 100vw;
            padding: 0.5rem;
          }
          .controls {
            flex-direction: column;
            gap: 0.25rem;
          }
        }
      `}</style>
    </div>
  );
}
