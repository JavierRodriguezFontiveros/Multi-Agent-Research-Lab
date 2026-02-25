from typing import Annotated, List, TypedDict
import operator

class AgentState(TypedDict):
    task: str
    plan: List[str]
    draft: str
    critique: str
    final_summary: str  # Para el resultado del resumidor
    # Annotated + operator.add permite que las listas se sumen
    content_sources: Annotated[List[str], operator.add] 
    revision_count: int