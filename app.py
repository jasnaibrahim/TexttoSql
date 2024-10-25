import streamlit as st
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType
from langchain_core.messages import SystemMessage
import config
from psycopg2 import OperationalError  # For error handling with PostgreSQL

from db import create_database_connection

def initialize_llm():
    """
    Initialize the Large Language Model (LLM) with the Groq API and the specified model name.

    Returns:
        ChatGroq: Configured LLM instance.
    """
    return ChatGroq(
        model_name="llama-3.1-70b-versatile",
        groq_api_key=config.GROQ_API_KEY,
        streaming=True,
      
    )

def create_agent_executor(db, llm):
    """
    Create and configure the SQL agent executor using the database connection and LLM.

    Args:
        db (SQLDatabase): The database connection.
        llm (ChatGroq): The initialized language model.

    Returns:
        AgentExecutor: The configured SQL agent executor.
    """
    SQL_PREFIX = """
    You are an AI assistant designed to help users interact with an Odoo PostgreSQL database...
    """

    system_message = SystemMessage(content=SQL_PREFIX)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        messages_modifier=system_message,
        # handle_parsing_errors=True
    )

def main():
    """
    Main function to run the Streamlit app, managing user interactions and displaying responses.
    """
    # Streamlit app configuration
    st.set_page_config(page_title="Chat with SQL DB")
    st.title("Chat with the Database")

    # Set up database connection
    try:
        db = create_database_connection()
    except OperationalError as e:
        st.error(str(e))
        st.stop()

    # Initialize LLM and agent executor
    llm = initialize_llm()
    agent_executor = create_agent_executor(db, llm)

    # Initialize message history in Streamlit session state
    if "messages" not in st.session_state or st.sidebar.button("Clear Message History"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Handle user query input
    user_query = st.chat_input(placeholder="Ask anything from the database")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        # Respond to user input using the LLM and SQL agent
        with st.chat_message("assistant"):
            try:
                streamlit_callback = StreamlitCallbackHandler(st.container())
                response = agent_executor.invoke(user_query, callbacks=[streamlit_callback])

                # Handle large datasets: suggest pagination or batch processing
                if isinstance(response, dict) and len(response.get("output", "")) > 1000:
                    response["output"] = "Your query returned a large result set. Consider refining your query or using pagination."

                st.session_state.messages.append({"role": "assistant", "content": response["output"]})
                st.write(response["output"])
            
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                st.error(error_message)

if __name__ == "__main__":
    main()
