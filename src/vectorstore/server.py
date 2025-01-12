from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import os

# Load the FAISS vectorstore with the code documents
loader = FileSystemBlobLoader(
    path=os.path.join(os.path.dirname(__file__), "documents"),
    glob="**/*.py",
    show_progress=True
)
docs = [Document(page_content=blob.as_string()) for blob in loader.yield_blobs()]
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
splits = text_splitter.split_documents(documents=docs)

vectorstore = FAISS.from_documents(documents=splits, embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))

# Define the FastAPI app
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/retrieve")
async def retrieve(request: QueryRequest):
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Query not provided")

    # Retrieve relevant documents from the vectorstore
    retriever = vectorstore.as_retriever()
    documents = retriever.invoke(query)

    # Format the response
    response = [{"text": doc.page_content} for doc in documents]
    return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)