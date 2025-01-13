#!/bin/bash
set -e

function stop {
    echo "Shutting down the Ollama service"
    ./src/llm/stop-llama-service.sh

    if [ -z "$VECTORSTORE_PID" ]; then
        echo "Vectorstore server is not running"
    else
        echo "Shutting down the Vectorstore server"
        kill $VECTORSTORE_PID
        VECTORSTORE_PID=
    fi

    if [ -z "$CLIENT_PID" ]; then
        echo "Chatbot client is not running"
    else
        echo "Stopping the Chatbot client"
        kill $CLIENT_PID
        CLIENT_PID=
    fi

    # Deactivate the python virtual environment
    if [ ! -z "${VIRTUAL_ENV}" ]; then
        deactivate
    fi
}

# Stop the services when the script is interrupted
trap stop SIGINT SIGTERM EXIT ERR

if [ ! -d "logs" ]; then
    mkdir logs
fi

source venv/bin/activate

echo "Starting Ollama service"
./src/llm/start-llama-service.sh

echo "Starting Vectorstore Service"
python src/vectorstore/server.py &> logs/vectorstore-service.log &
VECTORSTORE_PID=$!

echo "Starting client"
python src/client/run.py &> logs/client.log &
CLIENT_PID=$!
echo "Open client at http://localhost:10000"

echo "Startup complete. Press Ctrl+C to stop"

# Let the script hang until it is interrupted
tail -f /dev/null