# 🛡️ Multi-Agent-Research-Lab

**Agentic-RAG-OS: Self-Correcting Research Pipeline**

Este proyecto implementa un sistema **multi-agente capaz de realizar investigación técnica profunda de forma autónoma**, utilizando exclusivamente **LLMs Open Source** y una **arquitectura de grafo cíclico con auto-corrección**.

---

# 🎯 Motivación del Proyecto

Los pipelines **RAG tradicionales** suelen fallar ante:

- consultas complejas  
- información contradictoria  
- falta de verificación de fuentes  

Este sistema resuelve el problema mediante un flujo **Plan → Execute → Verify**, donde un **agente crítico** valida la veracidad de las respuestas antes de darlas por finalizadas.

Esto reduce las **alucinaciones en aproximadamente un ~30%** (estimado mediante evaluaciones en Langfuse).

---

# 🏗️ Arquitectura del Sistema

## Componentes Clave

**Orquestación**
- LangGraph para gestionar el estado y la lógica de re-intento (loops)

**Inferencia Local**
- Integración con Hugging Face mediante **vLLM / Ollama**
- Modelos utilizados:
  - Llama-3.1-8B
  - Mistral-Nemo

**Memoria & Estado**
- Uso de **TypedDict** para mantener:
  - el hilo de investigación
  - las fuentes recuperadas

**Observabilidad**
- **Langfuse** para:
  - tracing completo
  - gestión de prompts
  - evaluación de fidelidad (Faithfulness)

---

# 🛠️ Stack Tecnológico

| Capa | Herramienta | Razón de elección |
|-----|-------------|-------------------|
| Agentes | LangGraph | Soporta ciclos y persistencia de estado mejor que LangChain puro |
| Modelos (LLM) | Llama-3.1-8B | Buen equilibrio entre latencia y seguimiento de instrucciones en local |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 | Alta eficiencia en CPU/GPU |
| Database | ChromaDB / Qdrant | Vector store ligero y open-source |
| Monitoring | Langfuse | Tracing de pasos intermedios y debugging de agent thoughts |

---

# 🚀 Lógica de Auto-Corrección (The Router)

El núcleo del proyecto es la capacidad del sistema para **decidir si una investigación es suficiente**.

Implementamos una **arista condicional** basada en la evaluación del nodo **Reviewer**.

```python
def route_after_review(state: AgentState):
    # Lógica de decisión técnica
    
    if state["revisions_count"] >= 3:
        return "finalizer"  # salida de seguridad por límite de intentos
    
    if "FAIL" in state["critique"]:
        return "researcher" # reintento de búsqueda con feedback
    
    return "finalizer"      # aprobado
```

Este sistema permite:

- reintentar investigaciones incompletas  
- evitar loops infinitos  
- garantizar una respuesta validada

---

# 📈 Observabilidad y Evaluación

A diferencia de otros proyectos, este incluye una suite de evaluación **LLM-as-a-Judge**.

### Características

**Traceability**
- Cada ejecución genera un **ID único en Langfuse**

**Dataset Testing**
- Dataset interno de **20 preguntas complejas**
- Permite medir el **Success Rate** del pipeline de revisión

---

# 🛠️ Instalación y Uso Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/agentic-rag-os.git

# Instalar dependencias (Python 3.10+ recomendado)
pip install -r requirements.txt

# Levantar servicios (Langfuse + VectorDB)
docker-compose up -d

# Ejecutar el agente
python main.py --query "Explica las vulnerabilidades de reentrada en Solidity"
```

---

# 🧠 Lecciones Aprendidas

**Cuantización**
- El uso de modelos en **4-bit** puede afectar la capacidad de razonamiento del agente planificador.

**Control de Bucles**
- Es crucial mantener **contadores de estado** para evitar loops infinitos en grafos cíclicos.

**Prompt Engineering**
- Existen diferencias importantes entre prompts diseñados para:
  - modelos OpenAI
  - modelos open-source como Llama-3 en local

---

# 📌 Futuras Mejoras

- Integración con **rerankers neuronales**
- Mejor sistema de evaluación automática
- Soporte para **multi-document reasoning**
- UI para visualización del grafo de agentes

---

# 📜 Licencia

MIT License