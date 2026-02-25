from src.rag.vector_store import RAGManager
import os

def preparar_memoria():
    print("🧠 Preparando la memoria del Investigador...")
    
    # Asegurarnos de que existe la carpeta data
    if not os.path.exists("data"):
        os.makedirs("data")
        print("📂 Carpeta 'data/' creada. Por favor, mete tus PDFs ahí y vuelve a ejecutar.")
        return

    # Inicializar el gestor de RAG
    rag = RAGManager(data_path="data", db_path="db")
    
    # Procesar los documentos
    resultado = rag.ingest_docs()
    print(resultado)
    print("✨ ¡Listo! Ahora el Investigador podrá consultar estos documentos.")

if __name__ == "__main__":
    preparar_memoria()