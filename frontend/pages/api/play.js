import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const r = await axios.post('http://127.0.0.1:8000/play', req.body);
      res.status(200).json(r.data);
    } catch (e) {
      res.status(500).json({ status: 'error' });
    }
  } else {
    res.status(405).end();
  }
}
