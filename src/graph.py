from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.llm_config import model_researcher, model_critic, model_summarizer # <--- AÑADIDO
from src.nodes import ResearchLabNodes

class ResearchGraph:
    def __init__(self):
        # 1. Instanciamos con los TRES modelos
        self.nodes = ResearchLabNodes(model_researcher, model_critic, model_summarizer)
        self.workflow = StateGraph(AgentState)
        self._build_graph()
        self.app = self.workflow.compile()

    def _should_continue(self, state: AgentState):
        critique = state.get("critique", "").upper()
        count = state.get("revision_count", 0)
        
        # Si está aprobado o llegamos al límite, vamos al resumidor
        if "APROBADO" in critique or count >= 3:
            return "summarize" 
        return "continue"

    def _build_graph(self):
        self.workflow.add_node("investigador", self.nodes.researcher_node)
        self.workflow.add_node("critico", self.nodes.critic_node)
        self.workflow.add_node("resumidor", self.nodes.summarizer_node) 

        self.workflow.set_entry_point("investigador")
        self.workflow.add_edge("investigador", "critico")

        self.workflow.add_conditional_edges(
            "critico",
            self._should_continue,
            {
                "continue": "investigador", 
                "summarize": "resumidor", 
            }
        )
        
        # El resumidor siempre termina el proceso
        self.workflow.add_edge("resumidor", END)

    def run(self, inputs: dict, config: dict = None):
        return self.app.invoke(inputs, config=config)

research_pipeline = ResearchGraph()