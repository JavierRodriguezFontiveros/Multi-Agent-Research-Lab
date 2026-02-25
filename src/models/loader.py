import requests
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration # <--- IMPORTANTE
from typing import Any, List, Optional

class HFRouterModel(BaseChatModel):
    model_id: str
    hf_token: str

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        url = "https://router.huggingface.co/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.hf_token}", "Content-Type": "application/json"}
        
        # Mapeo de roles
        formatted_messages = []
        for m in messages:
            role = "user" if m.type == "human" else "assistant" if m.type == "ai" else m.type
            formatted_messages.append({"role": role, "content": m.content})

        payload = {
            "model": self.model_id,
            "messages": formatted_messages
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        res_json = response.json()
        content = res_json["choices"][0]["message"]["content"]
        
        # --- ESTRUCTURA CORRECTA PARA LANGCHAIN/LANGFUSE ---
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "hf_router"