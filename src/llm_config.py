import os
from dotenv import load_dotenv
from src.models.loader import HFRouterModel

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Instanciamos los tres roles
model_researcher = HFRouterModel(model_id="openai/gpt-oss-120b", hf_token=HF_TOKEN)
model_critic = HFRouterModel(model_id="openai/gpt-oss-120b", hf_token=HF_TOKEN)
model_summarizer = HFRouterModel(model_id="openai/gpt-oss-120b", hf_token=HF_TOKEN)