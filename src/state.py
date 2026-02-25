from typing import Annotated, List, TypedDict
import operator

class AgentState(TypedDict):
    task: str
    plan: List[str]
    draft: str
    critique: str
    # Annotated + operator.add permite que las listas se sumen en lugar de sobrescribirse
    content_sources: Annotated[List[str], operator.add] 
    revision_count: int