#!/bin/bash
mkdir logs
source venv/bin/activate
./src/llm/start-llama-service.sh

echo "Starting Vectorstore Service"
python src/vectorstore/server.py &> logs/vectorstore-service.log &

echo "Starting Client"
python src/client/run.py &> logs/client.log &
echo "Open client at http://localhost:10000"

echo "Startup complete"