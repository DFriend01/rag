from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import OllamaLLM
from langchain.schema import BaseRetriever, Document
import requests

class APIRetriever(BaseRetriever):
    def _get_relevant_documents(self, query: str):
        response = requests.post("http://127.0.0.1:5000/retrieve", json={"query": query})
        response.raise_for_status()
        documents = response.json()["documents"]
        return [Document(page_content=document["text"]) for document in documents]


llm = OllamaLLM(base_url="http://127.0.0.1:11434", model="llama3.2:3b")
retriever = APIRetriever()

# Contextualize question
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# Answer question
qa_system_prompt = (
    "You are an assistant for question-answering tasks. Use "
    "the following pieces of retrieved context to answer the "
    "question. If you don't know the answer, just say that you "
    "don't know. Use three sentences maximum and keep the answer "
    "concise."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Below we use create_stuff_documents_chain to feed all retrieved context
# into the LLM. Note that we can also use StuffDocumentsChain and other
# instances of BaseCombineDocumentsChain.
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

if __name__ == "__main__":
    query = None
    chat_history = []
    while (query != "quit"):
        query = input("You: ")
        if query == "quit":
            break

        result = rag_chain.invoke({"input": query, "chat_history": chat_history})
        response = result["answer"]

        print(f"Bot: {response}")

        chat_history.append(("human", query))
        chat_history.append(("ai", response))
