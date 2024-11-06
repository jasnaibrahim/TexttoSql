from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from psycopg2 import OperationalError  # For error handling with PostgreSQL
import streamlit as st

@st.cache_resource(ttl="1h")  # Cache for 1 hour (3600 seconds)
def create_database_connection():
    """
    Establish a connection to the PostgreSQL database using SQLAlchemy and LangChain's SQLDatabase utility.

    Returns:
        SQLDatabase: A connection to the database if successful; otherwise, raises an OperationalError.
    """
    try:
        # Fetch the database URI from Streamlit secrets
        database_uri = st.secrets["DATABASE_URI"]
        
        # Create the SQLAlchemy engine and establish a connection
        db = SQLDatabase(create_engine(database_uri))
        return db
    except OperationalError:
        raise OperationalError("Database connection failed. Please check your credentials or network connection.")
