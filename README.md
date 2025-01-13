# RAG with LangChain

A simple RAG system built with [LangChain](https://www.langchain.com/) and [Llama](https://www.llama.com/).
The goal was to learn about the various tools available to build RAGs while also self hosting open-source
LLMs.

The system is composed of three components:

1. Ollama Service (`src/llm`): Runs the Ollama service which is responsible for running LLMs locally.
2. Vectorstore Server (`src/vectorstore`): A FastAPI server containing a vectorstore responsible for fetching
relevant documents based on a user query.
3. Chatbot UI (`src/client`): A webpage that provides a chat interface to use the RAG.

## How to run

### Prerequisites

1. This system was programmed for Linux. Ubuntu 22.04 was used, but any recent Ubuntu or Debian distro
should probably be fine. If you're using Windows, running on
[WSL2](https://learn.microsoft.com/en-us/windows/wsl/about) should work fine.
2. Python should be installed. Python 3.10 was used to develop the RAG. If you're using Ubuntu, Python should
already be installed.

### Installing Dependencies

The setup script should install all the dependencies needed to run the RAG:

```bash
git clone https://github.com/DFriend01/rag.git rag
cd rag
./setup.sh
```

The setup script assumes that:

1. You're running on a debian distro
2. The `curl` and `python3` commands are available
3. You're a superuser

### Adding your documents

You can drop any code files in `src/vectorstore/documents`, which will be processed and added to the
vectorstore. This allows the RAG to retrieve relevant documents.

> [!WARNING]
> Documents are expected to be encoded with the UTF-8 character set. In other words, files
> encoded as plain text that contains the UTF-8 character set.
> Binary files (i.e. ".pdf", ".docx", etc.) cannot be encoded using this RAG implementation.
> Make sure to check the generated logs `logs/vectorstore-service.log` if you are experiencing
> any issues.

The file `src/vectorstore/config.yaml` configures how documents are chunked and which files are added
to the vectorstore. When adding your own documents, edit this configuration file to add any constraints
on which files to include or exclude. The following is an example configuration:

```yaml
document_matching:
    # Accept all .py and .md files. Leave empty to read all files.
    allowed_file_extensions: [".py", ".md"]
    # Ignore directories that are named "foo"
    excluded: ["**/foo/*"]
```

### Running the RAG

Run the system with `./run.sh`. The first run will take some time to set up. Once it is complete,
open `http://localhost:10000` in your favourite browser and ask the chatbot about your documents!

Use `CTRL + C` to stop the RAG. Sometimes, not all of the processes will stop so you should check
your processes to make sure they stopped using
[`ps`](https://linuxjourney.com/lesson/monitor-processes-ps-command) and
[`kill`](https://linuxjourney.com/lesson/killing-processes).

An example of how to do this:

```bash
# List your processes, if you see something like the first three listed, then stop them
> ps -au
USER      PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
user    27659  0.0  0.0   4920  3748 pts/0    S+   00:18   0:00 /bin/bash ./run.sh
user    27780 20.3 14.4 27987540 1152584 pts/0 Sl+ 00:18   0:13 python src/vectorstore/server.py
user    27781  8.3  2.2 901180 181000 pts/0   Sl+  00:18   0:05 python src/client/run.py
user    27782  0.0  0.0   3248  1000 pts/0    S+   00:18   0:00 tail -f /dev/null
user    28224  0.0  0.0   7488  3224 pts/2    R+   00:19   0:00 ps -au

# Stop the processes that are running the run.sh script, vectorstore, and client
# using the PIDs
> kill 27659 27780 27781
```

## Resources

- [arXiv: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [LangChain Blog Post: Deconstructing RAG](https://blog.langchain.dev/deconstructing-rag/)
- [Medium Article by Alex Fuentes: A Guide to Building RAG](https://falexm.medium.com/a-guide-to-building-rag-e2bf36d90035)
- [LangChain Cookbook on GitHub](https://github.com/langchain-ai/langchain/tree/master/cookbook)
- [Llama Recipes Quickstart on GitHub](https://github.com/meta-llama/llama-recipes/tree/main/recipes/quickstart)
