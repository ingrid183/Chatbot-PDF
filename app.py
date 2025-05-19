from langchain_ollama import ChatOllama
import streamlit as st

from rag import get_response_model

st.title('Ollama Chatbot')
st.write('Explora Streamlit')

if 'model_selection' not in st.session_state:
    st.session_state.model_selection = 'gemma3:12b'

if 'historial' not in st.session_state:
    st.session_state.historial = []

with st.sidebar:

    st.session_state.temperature = st.slider(
        'Temperatura',
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )
    st.session_state.top_p = st.slider(
        'Top P',
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.1
    )
    st.session_state.top_k = st.slider(
        'Top K',
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )
    st.session_state.max_tokens = st.slider(
        'Max Tokens',
        min_value=1,
        max_value=4096,
        value=256,
        step=1
    )

user_input = st.chat_input('Haz tu pregunta: ')

if user_input is not None:
    # Mostrar pregunta inmediatamente
    with st.chat_message("user"):
        st.write(user_input)
    
    try:
        # Obtener respuesta del modelo
        with st.spinner("🧠 El modelo está pensando..."):
            response = get_response_model(user_input)
            
            # Añadir respuesta al historial
            st.session_state.historial.append({
                "role": "assistant",
                "content": response['answer'],
            })
            
            # Mostrar respuesta
            with st.chat_message("assistant"):
                st.write(response['answer'])
                # st.caption(f"Modelo: {llm.model} | Tokens: {response.tokens} | Tiempo: {response.time}s")
                
    except Exception as e:
        st.error(f"Error: {e}")
