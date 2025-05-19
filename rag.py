from dotenv import load_dotenv
import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.vectorstores import InMemoryVectorStore
import bs4
from langchain import hub
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_chroma import Chroma


embeddings = OllamaEmbeddings(model="nomic-embed-text")

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")


vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

llm = ChatOllama(
    model = "qwen:4b",
    temperature = 0.0,
    num_predict = 256,
    top_p=0.5,
)

# 1. Cargar el PDF
loader = PyPDFLoader(r"C:\Users\Ingrid\Documents\ACTIVIDAD_1\ejemplo.pdf")  # ejemplo: "data/mi_archivo.pdf"
documents = loader.load()

# 2. Dividir el texto en fragmentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # Tamaño máximo del fragmento
    chunk_overlap=50     # Superposición entre fragmentos
)
split_docs = text_splitter.split_documents(documents)

_ = vector_store.add_documents(documents=split_docs)

# Verificar

# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")

# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    print('State: ')
    print(state)
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    print('State 2')
    print(state)
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
# * Hace los llamados para LangSmith
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

def get_response_model(user_input):
    response = graph.invoke({"question": user_input})
    return response

