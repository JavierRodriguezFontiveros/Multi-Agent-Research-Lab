from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.llm_config import model_researcher, model_critic
from src.nodes import ResearchLabNodes # Cambiado al nombre que usamos en la clase de nodes

class ResearchGraph:
    def __init__(self):
        # 1. Instanciamos la fábrica de nodos (Composición de objetos)
        self.nodes = ResearchLabNodes(model_researcher, model_critic)
        
        # 2. Construimos el flujo
        self.workflow = StateGraph(AgentState)
        self._build_graph()
        
        # 3. Compilamos el grafo como un atributo privado
        self.app = self.workflow.compile()

    def _should_continue(self, state: AgentState):
        """Lógica de control interna (Router)"""
        critique = state.get("critique", "").upper()
        count = state.get("revision_count", 0)
        
        if "APROBADO" in critique or count >= 3:
            return "end"
        return "continue"

    def _build_graph(self):
        """Define la arquitectura del grafo"""
        # Añadir nodos usando los métodos del objeto nodes
        self.workflow.add_node("investigador", self.nodes.researcher_node)
        self.workflow.add_node("critico", self.nodes.critic_node)

        # Definir conexiones
        self.workflow.set_entry_point("investigador")
        self.workflow.add_edge("investigador", "critico")

        # Lógica condicional
        self.workflow.add_conditional_edges(
            "critico",
            self._should_continue,
            {
                "continue": "investigador", 
                "end": END
            }
        )

    def run(self, inputs: dict, config: dict = None):
        """Método público para ejecutar el pipeline"""
        return self.app.invoke(inputs, config=config)

# Instancia única para ser importada por main.py
research_pipeline = ResearchGraph()