from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

class SearchTool:
    def __init__(self):
        wrapper = DuckDuckGoSearchAPIWrapper(
            region="es-es",
            max_results=5,
            safesearch="moderate",
            time="y"
        )

        self.search = DuckDuckGoSearchResults(api_wrapper=wrapper)

    def execute(self, query: str):
        """Busca información en internet y devuelve resultados estructurados."""
        print(f"🔍 Buscando en DuckDuckGo: {query}")
        return self.search.invoke(query)