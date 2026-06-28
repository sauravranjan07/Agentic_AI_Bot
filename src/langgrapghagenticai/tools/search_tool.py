from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Get the list of tools to be used in the graph
    """
    # Configure TavilySearch with proper API key and settings
    tavily_search = TavilySearch(
        max_results=5,
        include_answer=True,
        include_raw_content=False
    )
    
    tools = [tavily_search]
    return tools

def create_tool_node(tools):
    """
    Create a ToolNode with the given tools
    """
    tool_node = ToolNode(tools=tools)
    return tool_node