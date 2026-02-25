import os
import time
from dotenv import load_dotenv
from langfuse.callback import CallbackHandler

load_dotenv()

# Configuración
handler = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY").strip(),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY").strip(),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3000").strip()
)

def ejecutar_test_avanzado():
    print("🚀 Iniciando Simulación de Pipeline Multi-Agente...")
    
    # 1. LA TRAZA (El contenedor de todo el proceso)
    trace = handler.langfuse.trace(
        name="Pipeline de Investigación Completo",
        input={"query": "¿Por qué el cielo es azul?"},
        tags=["produccion-test", "multi-agente"]
    )

    # 2. PRIMER NODO: INVESTIGADOR
    print("🔍 Nodo 1: Investigador...")
    span_inv = trace.span(name="Agente_Investigador", input="Buscando dispersión de Rayleigh")
    time.sleep(1)
    
    # Simulamos que el investigador usa una HERRAMIENTA (Google Search)
    tool_span = span_inv.span(name="Tool: Google_Search", input="dispersión de Rayleigh física")
    time.sleep(0.5)
    tool_span.end(output="Resultados encontrados: 1.2M")
    
    span_inv.end(output="Borrador inicial generado.")

    # 3. SEGUNDO NODO: CRÍTICO (Generación de LLM)
    print("⚖️ Nodo 2: Crítico...")
    generation = trace.generation(
        name="Agente_Critico",
        model="gpt-4o",
        model_parameters={"temperature": 0.2},
        input="Borrador inicial: El cielo es azul por el reflejo del mar.",
        metadata={"tokens_estimate": 150}
    )
    time.sleep(0.8)
    # El crítico rechaza la primera versión
    generation.end(output="RECHAZADO: El color no es por el reflejo del mar, es por la atmósfera.")

    # 4. TERCER NODO: CORRECTOR (Finalización)
    print("✍️ Nodo 3: Corrector Final...")
    span_corr = trace.span(name="Agente_Corrector", input="Corrigiendo según crítica")
    time.sleep(1.2)
    final_text = "El cielo es azul debido a la dispersión de la luz solar en la atmósfera..."
    span_corr.end(output=final_text)

    # Cerramos la traza principal
    trace.update(output={"resultado_final": final_text})
    
    print("⏳ Sincronizando con Langfuse...")
    handler.flush()
    print("\n✅ ¡LISTO! Mira la UI ahora.")

if __name__ == "__main__":
    ejecutar_test_avanzado()