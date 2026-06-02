import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Now keep your working LangChain code exactly as it was:
from langchain_community.tools import DuckDuckGoSearchRun # or DuckDuckGoSearchResults

def web_search_tool(query: str) -> str:
    """
    Executes a live search on DuckDuckGo using LangChain's structured parser,
    with compiler-level warning silencing active.
    """
    try:
        search = DuckDuckGoSearchRun()
        return search.invoke(query)
    except Exception as e:
        return f"I encountered a connectivity glitch while scanning the web: {e}"
    
