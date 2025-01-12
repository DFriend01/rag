#!/bin/bash
./src/llm/stop-llama-service.sh

# Send GET request to shutdown the vectorstore server
curl -k http://127.0.0.1:5000/shutdown
echo ""

echo "Shutting down client"
CLIENT_PID=$(netstat -tunlp | grep 127.0.0.1:10000 | awk '{print $7}' | cut -d "/" -f1)

if [ -z "$CLIENT_PID" ]; then
    echo "Client is not running"
else
    echo "Killing client with PID $CLIENT_PID"
    kill $CLIENT_PID
fi

echo "Shutdown complete"