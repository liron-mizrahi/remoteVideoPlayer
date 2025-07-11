import axios from 'axios';

export default function handler(req, res) {
  if (req.method === 'POST') {
    axios.post('http://localhost:8000/mute')
      .then(r => res.status(200).json(r.data))
      .catch(() => res.status(500).json({ status: 'error' }));
  } else {
    res.status(405).end();
  }
}
