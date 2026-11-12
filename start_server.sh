#!/bin/bash
# A robust script to start and keep the uvicorn server alive
cd /home/jerry/codebase/wisedrama
source venv/bin/activate
while true; do
    echo "Starting Uvicorn Server at $(date)..." >> logs/server_monitor.log
    python src/api/server.py >> logs/uvicorn.log 2>&1
    echo "Server crashed with exit code $?. Respawning in 3 seconds..." >> logs/server_monitor.log
    sleep 3
done
