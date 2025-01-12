#!/bin/bash
./src/llm/stop-llama-service.sh

# Send GET request to shutdown the vectorstore server
curl -k http://127.0.0.1:5000/shutdown
echo ""

echo "Shutdown complete"