import os

def test_langfuse_v3():
    print("🚀 Probando integración Langfuse 3.x + LangChain...")
    print("-" * 40)

    try:
        # En la v3 con el paquete langfuse-langchain, esta es la ruta oficial:
        from langfuse.callback import CallbackHandler
        
        handler = CallbackHandler(
            public_key="test", 
            private_key="test", 
            host="http://localhost:3000"
        )
        print("✅ ¡CONSEGUIDO! CallbackHandler detectado e instanciado.")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Intenta: 'from langfuse.langchain import CallbackHandler' si lo anterior falla.")
    except Exception as e:
        print(f"✅ Librería detectada. (Aviso de configuración: {e})")

if __name__ == "__main__":
    test_langfuse_v3()