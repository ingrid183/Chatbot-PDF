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
import tempfile

embeddings = OllamaEmbeddings(model="nomic-embed-text")

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

llm = ChatOllama(
    model = "gemma3:12b",
    temperature = 0.0,
    num_predict = 256,
    top_p=0.5,
)


# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")

# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State, vector_store):
    print('State: ')
    print(state)
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])

    messages = [
        {"role": "system", "content": "Responde en español. Eres un experto en análisis de documentos PDF y debes responder con base en el contexto proporcionado."},
        {"role": "user", "content": f"Pregunta: {state['question']}\n\nContexto:\n{docs_content}"},
    ]

    response = llm.invoke(messages)
    return {"answer": response.content}



def get_response_model(user_input, uploaded_pdf):
    # Guardar PDF temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.read())
        tmp_path = tmp.name

    # Procesar PDF
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    # Dividir el texto
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)

    # Crear vectorstore temporal (RAM)
    vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )

    # Crear el grafo con pasos
    graph_builder = StateGraph(State)
    graph_builder.add_node("retrieve", lambda s: retrieve(s, vector_store))
    graph_builder.add_node("generate", generate)
    graph_builder.set_entry_point("retrieve")
    graph_builder.add_edge("retrieve", "generate")
    graph = graph_builder.compile()

    response = graph.invoke({"question": user_input})
    return response


