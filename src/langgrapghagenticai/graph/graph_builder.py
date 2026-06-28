
from langgraph.graph import StateGraph,START,END
from src.langgrapghagenticai.state.state import State
from src.langgrapghagenticai.nodes.basic_chatbot_node import BasicChatBotNode
from src.langgrapghagenticai.tools.search_tool import get_tools,create_tool_node
from src.langgrapghagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgrapghagenticai.nodes.ai_news_node import AINewsNode

from langgraph.prebuilt import tools_condition,ToolNode
class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)


    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph suing Langgraph.
        This method initialises a chatbot node using the 'BasicChatBotNode' class
        and integrates into the graph. the chatbot node is set as both the entry and exit point of grapgh
        """
        self.basic_chatbot_node = BasicChatBotNode(self.llm)  # Also fixed typo: bsasic -> basic
        
        self.graph_builder.add_node("chatnode", lambda state: self.basic_chatbot_node.process(state))
        self.graph_builder.add_edge(START, "chatnode")
        self.graph_builder.add_edge("chatnode", END) 
        
    def chatbot_with_web_build_graph(self):
        """
        Builds a chatbot with web access graph using Langgraph.
        This method initialises a chatbot node and a web access node, and integrates them into the graph. 
        The chatbot node is set as the entry point, and the web access node is set as the exit point of the graph.
        """
        tools = get_tools()
        tool_node = create_tool_node(tools)
        
        obj_chatbot_with_node = ChatbotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)
        
        self.graph_builder.add_node("chatnode", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        
        self.graph_builder.add_edge(START, "chatnode")
        self.graph_builder.add_conditional_edges("chatnode", tools_condition)
        self.graph_builder.add_edge("tools", "chatnode")  

    def ai_news_builder_graph(self):

        ai_news_node=AINewsNode(self.llm)

        ## added the nodes

        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_result)

        #added the edges

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result", END)

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot With Web":
            self.chatbot_with_tools_build_graph()
        if usecase == "AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()