import axios from 'axios';

export default function handler(req, res) {
  if (req.method === 'GET') {
    axios.get('http://localhost:8000/videos')
      .then(r => res.status(200).json(r.data))
      .catch(() => res.status(500).json([]));
  } else {
    res.status(405).end();
  }
}
