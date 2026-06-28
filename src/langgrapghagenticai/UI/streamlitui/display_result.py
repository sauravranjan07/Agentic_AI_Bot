import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        
        try:
            if usecase == "Basic Chatbot":
                # Display user message
                with st.chat_message("user"):
                    st.write(user_message)
                
                # Stream assistant response
                with st.chat_message("assistant"):
                    assistant_response = ""
                    
                    for event in graph.stream({'messages': [HumanMessage(content=user_message)]}):
                        for node_name, value in event.items():
                            if isinstance(value, dict) and 'messages' in value:
                                messages = value['messages']
                                if messages and len(messages) > 0:
                                    last_message = messages[-1]
                                    
                                    # Only show AI messages
                                    if isinstance(last_message, AIMessage):
                                        assistant_response = last_message.content
                    
                    # Display the complete assistant response
                    if assistant_response:
                        st.write(assistant_response)
                    else:
                        st.write("No response received from assistant")

            elif usecase == "Chatbot with Web":
                # Display user message
                with st.chat_message("user"):
                    st.write(user_message)
                
                # Prepare state with HumanMessage object
                initial_state = {"messages": [HumanMessage(content=user_message)]}
                
                try:
                    res = graph.invoke(initial_state)
                    
                    # Display all messages from response
                    if res and 'messages' in res:
                        messages = res['messages']
                        
                        for message in messages:
                            # Skip the initial user message if it appears again
                            if isinstance(message, HumanMessage):
                                continue
                            elif isinstance(message, ToolMessage):
                                with st.chat_message("assistant"):
                                    st.write("🔧 Tool Result:")
                                    st.write(message.content)
                            elif isinstance(message, AIMessage):
                                if message.content:
                                    with st.chat_message("assistant"):
                                        st.write(message.content)
                    else:
                        st.warning("No response from graph")
                        
                except Exception as e:
                    st.error(f"Error invoking graph: {str(e)}")
            
            elif usecase == "AI News":
                frequency = self.user_message
                with st.spinner("Fetching and summarizing news... ⏳"):
                    result = graph.invoke({"messages": [HumanMessage(content=frequency)]})
                    try:
                        # Read the markdown file
                        AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                        with open(AI_NEWS_PATH, "r") as file:
                            markdown_content = file.read()

                        # Display the markdown content in Streamlit
                        st.markdown(markdown_content, unsafe_allow_html=True)
                    except FileNotFoundError:
                        st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.error(f"Unknown usecase: {usecase}")
                
        except Exception as e:
            st.error(f"Error displaying result: {str(e)}")
            print(f"Detailed error: {e}")
            import traceback
            traceback.print_exc()