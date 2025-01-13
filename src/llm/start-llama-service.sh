#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/config.env

sudo systemctl start ollama

echo "Waiting ${SECONDS_TO_WAIT} seconds for Ollama service to start"
sleep ${SECONDS_TO_WAIT}

echo "Pulling model ${OLLAMA_MODEL}"
ollama pull ${OLLAMA_MODEL}
