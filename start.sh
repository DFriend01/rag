#!/bin/bash
mkdir logs
source venv/bin/activate
./src/llm/start-llama-service.sh
python src/vectorstore/server.py &> logs/vectorstore-service.log &
echo "Startup complete"