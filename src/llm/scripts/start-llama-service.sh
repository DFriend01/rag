#!/bin/bash
echo "Starting Ollama Service"
sudo systemctl start ollama

NSEC=5
echo "Waiting ${NSEC} seconds for service to start"
sleep ${NSEC}

echo "Pulling model ${OLLAMA_MODEL}"
ollama pull ${OLLAMA_MODEL}
