from src.state import AgentState

class ResearchLabNodes:
    def __init__(self, researcher, critic):
        self.researcher = researcher
        self.critic = critic

    def researcher_node(self, state: AgentState):
        print("--- INVESTIGADOR TRABAJANDO ---")
        res = self.researcher.invoke(f"Investiga sobre: {state['task']}. Sé técnico.")
        return {
            "draft": res.content, 
            "revision_count": state.get("revision_count", 0) + 1
        }

    def critic_node(self, state: AgentState):
        print("--- CRÍTICO EVALUANDO ---")
        res = self.critic.invoke(
            f"Evalúa este texto. Si es perfecto responde 'APROBADO'. Si no, da feedback:\n{state['draft']}"
        )
        return {"critique": res.content}