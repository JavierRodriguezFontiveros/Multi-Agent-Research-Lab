import os
from dotenv import load_dotenv
from langfuse import Langfuse
from src.graph import research_pipeline
from langfuse.callback import CallbackHandler

class ResearchApp:
    def __init__(self):
        """Inicializa la aplicación y carga la configuración."""
        load_dotenv()
        self.hf_token = os.getenv("HF_TOKEN")
        self.lf_host = os.getenv("LANGFUSE_HOST", "http://localhost:3000").strip().replace('"', '')
        self.client = None

        try:
            # Inicialización compatible v2.x
            self.client = Langfuse(
                secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                host=self.lf_host
            )
            print("✅ Langfuse inicializado correctamente")
        except Exception as e:
            print(f"⚠️ Error inicializando Langfuse: {e}")

    def check_environment(self):
        """Verifica servicios adicionales (HF)."""
        if not self.hf_token:
            raise ValueError("❌ Error: HF_TOKEN no encontrado en el archivo .env")
        print("✅ Hugging Face Token: Configurado")

    def run(self, query: str):
        self.check_environment()
        
        inputs = {
            "task": query,
            "revision_count": 0,
            "content_sources": []
        }

        if self.client:
            try:
                # 1. Creamos el CallbackHandler para que LangGraph "auto-registre" todo
                # Usamos las mismas credenciales que ya tienes
                handler = CallbackHandler(
                    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                    host=self.lf_host
                )
                
                # 2. Creamos la traza principal (opcional, ayuda a agrupar)
                # Pero lo importante es el handler en config
                print("--- INVESTIGADOR Y CRÍTICO TRABAJANDO (CON TRACING) ---")
                
                # 3. EJECUCIÓN: Pasamos el handler en el diccionario config
                final_state = research_pipeline.run(
                    inputs=inputs, 
                    config={"callbacks": [handler], "run_name": f"Investigación: {query}"}
                )
                
                self._print_results(final_state)
                
            except Exception as e:
                print(f"❌ Error durante la ejecución: {e}")
            finally:
                print("📡 Sincronizando datos con Langfuse...")
                self.client.flush()
        else:
            print("⚠️ Langfuse no disponible, ejecutando pipeline sin tracing")
            final_state = research_pipeline.run(inputs)
            self._print_results(final_state)

    def _print_results(self, state: dict):
        """Método privado para formatear la salida."""
        print("\n" + "="*30)
        print("✅ PROCESO FINALIZADO")
        print("="*30)
        print(f"Versiones realizadas: {state.get('revision_count')}")
        print(f"Resumen del resultado:\n{state.get('draft', '')[:500]}...")
        print("="*30)

if __name__ == "__main__":
    app = ResearchApp()
    pregunta = "¿Cuantos días tiene una semana?"
    app.run(pregunta)