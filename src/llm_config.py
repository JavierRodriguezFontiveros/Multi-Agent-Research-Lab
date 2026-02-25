import os
from dotenv import load_dotenv
from src.models.loader import HFRouterModel

load_dotenv()

# Usamos el token de tu .env o el que pusiste en el ejemplo
HF_TOKEN = os.getenv("HF_TOKEN")

# Instanciamos los objetos POO
model_researcher = HFRouterModel(model_id="openai/gpt-oss-120b", hf_token=HF_TOKEN)
model_critic = HFRouterModel(model_id="openai/gpt-oss-120b", hf_token=HF_TOKEN)