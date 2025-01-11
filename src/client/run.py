from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import bs4

loader = WebBaseLoader(["https://huggingface.co/blog/llama3"])
docs = loader.load()

# Split the document into chunks with a specified chunk size
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_splits = text_splitter.split_documents(docs)

# Store the document into a vector store with a specific embedding model
vectorstore = FAISS.from_documents(all_splits, HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))

from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

llm = OllamaLLM(base_url="http://127.0.0.1:11434", model="llama3.2:3b")
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever()
)

question = "What's new with Llama 3?"
result = qa_chain({"query": question})
print(result['result'])