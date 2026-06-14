import streamlit as st
from src.langgrapghagenticai.UI.streamlitui.loadui import LoadSreamlitUi

def load_langgraph_agentic_ai_app():
    ui=LoadSreamlitUi()
    user_input=ui.load_streamlit_ui()
    if not user_input:
        st.error("Error:Failed to load user input from UI")
        return
    user_message=st.chat_input('Enter your message')
    # if user_message:
    #     try:
    #         obj_llm_config=GroqLLM(user_controls_input=user_input)
    #         model=obj_llm_config.get_llm_model

    #         if not model:
    #             st.error("Error:failed to load LLM")
    #             return
    #         usecase=user_input.get("selected_usecase")
    #         if not usecase:
    #             st.error("Error:No usecase selected")
    #             return