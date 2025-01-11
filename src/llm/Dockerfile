FROM ubuntu:24.04
RUN apt update && apt install -y curl
RUN sh -c 'curl -fsSL https://ollama.com/install.sh | sh'

ENV LLAMA_MODEL="llama3.2:3b"

RUN eval "ollama serve &" \
    && sleep 5 \
    && ollama pull ${LLAMA_MODEL}
