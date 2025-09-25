from langchain_ollama import ChatOllama

# Tek LLM instance (her yerde kullanilacak)
llm_gemma = ChatOllama(
    model="gemma3:27b-it-qat",
    temperature=0
)
