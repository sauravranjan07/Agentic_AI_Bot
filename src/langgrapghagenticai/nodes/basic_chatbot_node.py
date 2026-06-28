from src.langgrapghagenticai.state.state import State
from langchain_core.messages import AIMessage

class BasicChatBotNode:
    """
    basic implementation of bot
    """
    def __init__(self, model):
        self.llm = model
    
    def process(self, state: State) -> dict:
        """
        process the structure of the state used in graph
        """
        messages = state['messages']
        response = self.llm.invoke(messages)
        return {"messages": [response]}