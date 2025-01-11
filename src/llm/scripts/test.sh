#!/bin/bash
curl --location http://localhost:11434/api/chat \
    --header 'Content-Type: application/json' \
    --data '{
            "model": "llama3.2:3b",
            "messages": [
                {
                "role": "user",
                "content": "who wrote the book godfather?"
                }
            ],
            "stream": false
        }'