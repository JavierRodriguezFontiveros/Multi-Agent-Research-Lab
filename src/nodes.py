from src.state import AgentState
from src.rag.vector_store import RAGManager
from langchain_community.tools import DuckDuckGoSearchRun 

class ResearchLabNodes:
    def __init__(self, researcher, critic, summarizer):
        self.researcher = researcher
        self.critic = critic
        self.summarizer = summarizer
        self.rag = RAGManager()
        # Inicializamos la herramienta de búsqueda
        self.search_tool = DuckDuckGoSearchRun()

    def researcher_node(self, state: AgentState):
        print("--- INVESTIGADOR BUSCANDO EN DOCUMENTOS (RAG) ---")
        contexto = self.rag.get_context(state['task'])
        
        prompt_enriquecido = f"""Usa el siguiente contexto para responder a la tarea de forma técnica. 
        CONTEXTO RECUPERADO:
        {contexto}
        
        TAREA:
        {state['task']}
        """
        res = self.researcher.invoke(prompt_enriquecido)
        return {
            "draft": res.content, 
            "revision_count": state.get("revision_count", 0) + 1,
            "content_sources": ["Base de Datos Vectorial (PDFs locales)"]
        }

    def critic_node(self, state: AgentState):
        print("--- CRÍTICO INVESTIGANDO EN INTERNET Y EVALUANDO ---")
        
        # 1. El crítico busca tendencias externas para comparar
        query_busqueda = f"tendencias actuales y apartados imprescindibles en {state['task']} 2026"
        search_results = self.search_tool.run(query_busqueda)
        
        # 2. El crítico evalúa el borrador frente a la info de internet
        prompt_critico = f"""Eres un experto evaluador. Tu tarea es comparar el borrador del Investigador con la información real de internet.
        
        INFORMACIÓN DE INTERNET:
        {search_results}
        
        BORRADOR DEL INVESTIGADOR:
        {state['draft']}
        
        Si el borrador es correcto y está actualizado según internet, responde únicamente 'APROBADO'.
        Si falta algo o hay errores, da feedback detallado para que el investigador lo corrija.
        """
        
        res = self.critic.invoke(prompt_critico)
        return {"critique": res.content}

    def summarizer_node(self, state: AgentState):
        print("--- RESUMIDOR REDACTANDO INFORME FINAL ---")
        draft = state.get("draft")
        task = state.get("task")
        
        prompt = f"""Eres un Editor Jefe. Tu misión es tomar la investigación final y presentarla de forma impecable.
        
        TAREA ORIGINAL: {task}
        INVESTIGACIÓN APROBADA: {draft}
        
        INSTRUCCIONES:
        1. Usa encabezados claros (##).
        2. Usa listas de puntos para las habilidades o apartados.
        3. Asegúrate de que no haya repeticiones.
        4. El resultado debe estar listo para ser presentado a un cliente o reclutador.
        """
        
        res = self.summarizer.invoke(prompt)
        return {"final_summary": res.content}