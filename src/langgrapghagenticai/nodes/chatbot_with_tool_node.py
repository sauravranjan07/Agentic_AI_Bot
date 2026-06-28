from src.langgrapghagenticai.state.state import State
from langchain_core.messages import SystemMessage

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    The LLM automatically decides when to use tools based on user query.
    """
    def __init__(self, model):
        self.llm = model

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function with tools bound.
        """
        llm_with_tools = self.llm.bind_tools(tools)
        
        system_message = SystemMessage(
            content="You are a helpful assistant. When users ask for news or web search, use the tavily_search tool with only a 'query' parameter. Keep responses concise."
        )

        def chatbot_node(state: State):
            """
            Chatbot logic with tool integration.
            """
            messages = state["messages"]
            # Add system message at the beginning if not already there
            if not messages or not isinstance(messages[0], SystemMessage):
                messages = [system_message] + messages
            
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}

        return chatbot_node