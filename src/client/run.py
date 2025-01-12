from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.schema import BaseRetriever, Document
import requests

class APIRetriever(BaseRetriever):
    def get_relevant_documents(self, query: str):
        response = requests.post("http://127.0.0.1:5000/retrieve", json={"query": query})
        response.raise_for_status()
        results = response.json()
        return [Document(page_content=result["text"]) for result in results]


llm = OllamaLLM(base_url="http://127.0.0.1:11434", model="llama3.2:3b")
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=APIRetriever()
)

query = ""
while query != "quit":
    query = input("Ask a question: ")
    result = qa_chain({"query": query})
    print(result['result'])
