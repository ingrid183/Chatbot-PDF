# Instrucciones del proyecto 
Estel proyecto es una interfaz web con Streamlit que permite lecturas de pdfs y realizar preguntas respecto a los pdf suministrados.


### 1. Descargar Ollama y uv
- Ollama - [Download](https://ollama.com/)
- uv - [Terminal](https://docs.astral.sh/uv/#__tabbed_1_1)
> [!IMPORTANT]
> Para correr satisfactoriamente la aplicación y configuración debes contar con UV Python y Ollama (LLMs Open Source).

### 2. Instalar modelos de Ollama: [Llama3](https://ollama.com/library/llama3)
```bash
# Validar Ollama descargado
ollama

# Descargar modelos Llama3
ollama run llama3


# Descargar modelo gemma3:12b
ollama pull gemma3:12b


# Descargar modelo embedding 
ollama pull nomic-embed-text
```

### 3. Clona el repositorio e instalar dependencias
```bash
git clone https://github.com/ingrid183/Chatbot-PDF
cd Chatbot-PDF

uv add
uv sync
```

### 4. Ejecutar el streamlit
```bash
uv run streamlit run app.py   
```

### 5. Ejemplos de ejecución

#### Ejemplo 1 documento 77344439046, Tema cambio climatico

![Ejemplo 1](./Data/Ejemplo1.jpg)

<br />

#### Ejemplo 2 documento ejemplo. Tema que es y partes de un PDF

![Ejemplo 2](./Data/Ejemplo2.jpg)



---

### :busts_in_silhouette: Autor:
- [@ingrid183](https://github.com/ingrid183)
