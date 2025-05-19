# Instrucciones del proyecto 
Estel proyecto es una interfaz web con Streamlit que permite lecturas de pdfs y realizar preguntas respecto a los pdf suministrados.


### 1. Descargar Ollama y uv
- Ollama - [Download](https://ollama.com/)
- uv - [Terminal](https://docs.astral.sh/uv/#__tabbed_1_1)
> [!IMPORTANT]
> Para correr satisfactoriamente la aplicación y configuración debes contar con UV Python y Ollama (LLMs Open Source).

### 2. Instalar modelo de Ollama: [Llama3](https://ollama.com/library/llama3)
```bash
# Validar Ollama descargado
ollama

# Descargar modelos Llama3
ollama run llama3

### 3. Clona el repositorio e instalar dependencias
```bash
git clone https:[//github.com/DonLuisM/languagesTranslate_Ollama.git
cd languagesTranslate_Ollama
](https://github.com/ingrid183/Chatbot-PDF)

uv add
uv sync
```

### 4. Ejecutar la aplicación
```bash
uv run app.py
```

### 5. Ejecutar el streamlit para comparar respuestas
```bash
uv run streamlit run .\streamlit\app_st_cont.py   
```
---

### :busts_in_silhouette: Autor:
- [@ingrid183](https://github.com/ingrid183)
