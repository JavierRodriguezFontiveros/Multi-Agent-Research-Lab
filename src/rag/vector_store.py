import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class RAGManager:
    def __init__(self, data_path="data", db_path="db"):
        self.data_path = data_path
        self.db_path = db_path
        # Usamos un modelo de embeddings pequeño que corre en TU CPU (gratis)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def ingest_docs(self):
        """Lee los documentos de /data y los guarda en la DB vectorial."""
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            return "Carpeta /data creada. Añade PDFs ahí."

        loader = DirectoryLoader(self.data_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()
        
        # Partimos el texto en trozos (chunks) para que el LLM no se sature
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Creamos o cargamos la DB en disco (persistente)
        self.vector_store = Chroma.from_documents(
            documents=splits, 
            embedding=self.embeddings,
            persist_directory=self.db_path
        )
        return f"✅ {len(splits)} fragmentos indexados correctamente."

    def get_context(self, query: str):
        """Busca los fragmentos más relevantes para una pregunta."""
        if not self.vector_store:
            # Si no hay DB en memoria, intentamos cargar la de disco
            self.vector_store = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)
            
        results = self.vector_store.similarity_search(query, k=3)
        return "\n\n".join([doc.page_content for doc in results])