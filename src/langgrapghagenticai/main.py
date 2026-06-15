import streamlit as st
from src.langgrapghagenticai.UI.streamlitui.loadui import LoadStreamlitUI
from src.langgrapghagenticai.LLMS.groqllm import GroqLLM
from src.langgrapghagenticai.graph.graph_builder import GraphBuilder
from src.langgrapghagenticai.UI.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agentic_ai_app():
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()
    if not user_input:
        st.error("Error:Failed to load user input from UI")
        return
    user_message=st.chat_input('Enter your message')
    if user_message:
        try:
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error:failed to load LLM")
                return
            usecase=user_input.get("selected_usecase")
            print(usecase)
            if not usecase:
                st.error("Error:No usecase selected")
                return
            
            # /Graph builder
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error:Graph setup failed.{e}")
                return
        except Exception as e:
             st.error(f"setup failed.{e}")
             return

