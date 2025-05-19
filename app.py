import streamlit as st
from rag import get_response_model

st.title('Ollama Chatbot con PDF')
st.write('Carga un PDF y haz preguntas en español')

if 'model_selection' not in st.session_state:
    st.session_state.model_selection = 'gemma3:12b'

if 'historial' not in st.session_state:
    st.session_state.historial = []

# Cargar PDF
pdf_file = st.file_uploader("Sube un PDF", type=["pdf"])

# Mostrar historial antes de nueva entrada
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        st.write(mensaje["content"])

# Configuración en sidebar
with st.sidebar:
    st.session_state.temperature = st.slider('Temperatura', 0.0, 1.0, 0.5, 0.1)
    st.session_state.top_p = st.slider('Top P', 0.0, 1.0, 0.9, 0.1)
    st.session_state.top_k = st.slider('Top K', 0, 100, 50, 1)
    st.session_state.max_tokens = st.slider('Max Tokens', 1, 4096, 256, 1)

# Entrada del usuario
user_input = st.chat_input('Haz tu pregunta: ')

if user_input and pdf_file:
    # Guardar mensaje del usuario
    st.session_state.historial.append({
        "role": "user",
        "content": user_input,
    })

    with st.chat_message("user"):
        st.write(user_input)

    try:
        with st.spinner("🧠 El modelo está pensando..."):
            response = get_response_model(user_input, pdf_file)

            # Añadir respuesta al historial
            st.session_state.historial.append({
                "role": "assistant",
                "content": response['answer'],
            })

            with st.chat_message("assistant"):
                st.write(response['answer'])

    except Exception as e:
        st.error(f"Error: {e}")

elif user_input and not pdf_file:
    st.warning("Por favor sube un archivo PDF antes de hacer preguntas.")
