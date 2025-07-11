#!/bin/bash
# Start backend and frontend in parallel

cd "$(dirname "$0")"

# Start frontend in background
(
  cd frontend
  npm install
  npm run dev
) &

# Start backend in foreground
cd ./
if [ -d .venv ]; then
  source .venv/bin/activate
fi
python main.py
