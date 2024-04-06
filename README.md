# Implement LangChain to read file PDF and answer question in Vietnamese
* Model: From huggingface.co, [click here to download model](https://huggingface.co/vilm/vinallama-7b-chat-GGUF)
* Convert file pdf to vector database: [Preprocessing data](/venv/prepare_vector_db.py)
* File train Q/A bot for specify context: [QAFromPDF.py](/venv/QAFromPDF.py)
* Source: [From Mi AI](https://www.youtube.com/watch?v=z1OfI_NOvgI). Thank!